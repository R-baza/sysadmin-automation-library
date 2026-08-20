import os
import re
import subprocess
from dotenv import load_dotenv
import requests

# Load environment variables from a .env file (expects 'discord_url')
load_dotenv()
WEBHOOK_URL = os.getenv("discord_url")

# Configuration constants
SSH_LOG_PATH = "/var/log/auth.log"
FAILED_LOGIN_THRESHOLD = 5


def send_discord_notification(message: str) -> None:
    """Sends a formatted alert message to a configured Discord webhook.

    Handles network exceptions gracefully to prevent script crashes.
    """
    if not WEBHOOK_URL:
        print("Warning: Discord webhook URL not found in environment variables.")
        return

    payload = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord webhook: {e}")


def parse_failed_logins(log_file_path: str) -> dict:
    """Parses an authentication log file and returns a dictionary

    mapping unique IP addresses to their total failed login count.
    """
    failed_ips = {}

    try:
        with open(log_file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
        return failed_ips

    # Regex pattern to capture the source IP from SSH failed password lines
    failed_ip_pattern = r"Failed password for (?:invalid user )?(?:[a-zA-Z0-9_\-]+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    
    ips = re.findall(failed_ip_pattern, content)

    # Tally occurrences of each failing IP
    for ip in ips:
        failed_ips[ip] = failed_ips.get(ip, 0) + 1

    return failed_ips


def main():
    """Main execution loop for analyzing logs and enforcing firewall rules."""
    print("Starting SSH Sentinel log analysis...")
    failed_ips = parse_failed_logins(SSH_LOG_PATH)
    
    print(f"Summary of failed attempts: {failed_ips}")

    if not failed_ips:
        print("No failed login attempts detected.")
        return

    # Evaluate IP counts against the threshold and execute defense actions
    for ip, count in failed_ips.items():
        if count > FAILED_LOGIN_THRESHOLD:
            print(f"Threshold exceeded for {ip} ({count} failures). Blocking via UFW...")
            
            # Apply UFW firewall block rule for SSH (port 22)
            subprocess.run(["ufw", "deny", "from", ip, "to", "any", "port", "22"], check=True)
            
            # Send notification
            alert_msg = f"🚨 **Security Alert:** Blocked IP `{ip}` after `{count}` failed SSH attempts."
            send_discord_notification(alert_msg)


if __name__ == "__main__":
    main()
                


