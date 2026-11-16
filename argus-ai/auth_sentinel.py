import os
import re
import sqlite3
import subprocess
from dotenv import load_dotenv
import requests

# Load environment variables (Discord Webhook URL)
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

LOG_PATH = "/tmp/auth.log"
DB_FILE = "ssh_attempts.db"


def init_db():
  """Initializes the SQLite database and creates required tables."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()

  # Table for individual failed attempts
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS failed_ssh_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            source_ip TEXT
        )
    """)

  # Table to track quarantined IPs so we don't spam duplicate rules
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT UNIQUE,
            blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  conn.commit()
  conn.close()


def parse_auth_log(path: str) -> list:
  """Parses SSH auth log for failed login attempts using regex."""
  failed_attempts = []
  pattern = re.compile(
      r"(?P<month>\w{3})\s+(?P<day>\d+)\s+(?P<time>[\d:]+).*Failed password for"
      r" (?:invalid user )?(?P<username>\S+) from (?P<source_ip>[\d\.]+)"
  )

  try:
    with open(path, "r") as f:
      for line in f:
        match = pattern.search(line)
        if match:
          data = match.groupdict()
          failed_attempts.append({
              "timestamp": f"{data['month']} {data['day']} {data['time']}",
              "username": data["username"],
              "source_ip": data["source_ip"],
          })
    print(f"[+] Found {len(failed_attempts)} failed login attempts in {path}.")
  except FileNotFoundError:
    print(f"[-] Log file not found at {path}. Check your path or permissions.")

  return failed_attempts


def save_to_db(failed_attempts: list):
  """Inserts parsed failed login records into the SQLite database."""
  if not failed_attempts:
    return

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()

  for attempt in failed_attempts:
    cursor.execute(
        """
            INSERT INTO failed_ssh_attempts (timestamp, username, source_ip)
            VALUES (?, ?, ?)
        """,
        (attempt["timestamp"], attempt["username"], attempt["source_ip"]),
    )

  conn.commit()
  conn.close()
  print("[+] Data saved to SQLite database.")


def is_already_blocked(ip_address: str) -> bool:
  """Checks if an IP has already been recorded as blocked in the database."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT 1 FROM blocked_ips WHERE source_ip = ?", (ip_address,)
  )
  result = cursor.fetchone()
  conn.close()
  return result is not None


def record_blocked_ip(ip_address: str):
  """Records a successfully blocked IP in the database."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute(
      "INSERT OR IGNORE INTO blocked_ips (source_ip) VALUES (?)", (ip_address,)
  )
  conn.commit()
  conn.close()


def block_ip_iptables(ip_address: str) -> bool:
  """Automatically adds an iptables DROP rule for the offending IP address."""
  if is_already_blocked(ip_address):
    print(
        f"[*] IP {ip_address} is already recorded as blocked. Skipping iptables"
        " command."
    )
    return True

  try:
    cmd = [
        "sudo",
        "iptables",
        "-A",
        "INPUT",
        "-s",
        ip_address,
        "-p",
        "tcp",
        "--dport",
        "22",
        "-j",
        "DROP",
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)

    print(
        f"[+] FIREWALL ACTION: Successfully dropped IP {ip_address} via iptables."
    )
    record_blocked_ip(ip_address)
    return True

  except subprocess.CalledProcessError as e:
    error_msg = e.stderr.strip()
    print(f"[-] Failed to block IP {ip_address} via iptables. Error: {error_msg}")
    return False


def process_security_events(failed_attempts: list, threshold: int = 3):
  """Counts failures per IP, triggers UFW block if threshold is breached, and alerts Discord."""
  if not failed_attempts:
    return

  ip_counts = {}
  for attempt in failed_attempts:
    ip = attempt["source_ip"]
    ip_counts[ip] = ip_counts.get(ip, 0) + 1

  for ip, count in ip_counts.items():
    if count >= threshold:
      print(
          f"[!] Threat detected: IP {ip} exceeded threshold with {count}"
          " failures."
      )

      # 1. Execute automated UFW firewall quarantine
      blocked = block_ip_iptables(ip)

      # 2. Dispatch Discord Webhook Alert
      if DISCORD_WEBHOOK_URL:
        status_note = (
            "🔒 **Action Taken:** IP automatically blocked via UFW."
            if blocked
            else "⚠️ **Action Failed:** Manual intervention required."
        )
        payload = {
            "content": (
                f"🚨 **SECURITY ALERT:** Brute-force threshold exceeded!\n"
                f"• **Source IP:** `{ip}`\n"
                f"• **Failed Attempts:** `{count}`\n"
                f"{status_note}"
            )
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
          print(f"[+] Discord alert sent for IP: {ip}")
        else:
          print(
              f"[-] Failed to send Discord alert. Status code:"
              f" {response.status_code}"
          )


if __name__ == "__main__":
  print("[*] Initializing Log Sentinel...")
  init_db()

  attempts = parse_auth_log(LOG_PATH)
  if attempts:
    save_to_db(attempts)
    process_security_events(attempts, threshold=3)
  else:
    print("[+] No failed login attempts parsed.")
