import os
import gzip
import shutil
import time
import logging
import requests
from dotenv import load_dotenv

# Load environment variables for optional Discord alerting
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        payload = {"content": f"🗄️ **Log Rotator Sentinel**\n{message}"}
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"Failed to send Discord alert: {e}")

def rotate_and_clean_logs(target_dir="/tmp", max_age_days=7, retention_days=30):
    logging.info(f"[*] Starting log rotation scan on: {target_dir}")
    
    now = time.time()
    age_threshold_seconds = max_age_days * 86400
    retention_threshold_seconds = retention_days * 86400
    
    compressed_count = 0
    cleaned_count = 0
    space_saved = 0

    try:
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            
            # Skip directories and already compressed files
            if os.path.isdir(file_path):
                continue
                
            file_mtime = os.path.getmtime(file_path)
            file_age = now - file_mtime
            
            # 1. Compress uncompressed log files older than max_age_days
            if not filename.endswith('.gz') and file_age > age_threshold_seconds:
                gz_path = file_path + '.gz'
                original_size = os.path.getsize(file_path)
                
                logging.info(f"[*] Compressing stale log: {filename}")
                with open(file_path, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                
                os.remove(file_path)
                compressed_count += 1
                space_saved += (original_size - os.path.getsize(gz_path))
            
            # 2. Prune old .gz archives exceeding the retention window
            elif filename.endswith('.gz') and file_age > retention_threshold_seconds:
                logging.info(f"[-] Deleting expired archive: {filename}")
                os.remove(file_path)
                cleaned_count += 1

        summary = (
            f"Successfully rotated {compressed_count} log(s) "
            f"and purged {cleaned_count} expired archive(s)."
        )
        logging.info(f"[+] {summary}")
        
        if compressed_count > 0 or cleaned_count > 0:
            send_discord_alert(summary)
            
    except Exception as e:
        err_msg = f"Error during log rotation execution: {e}"
        logging.error(err_msg)
        send_discord_alert(f"⚠️ {err_msg}")

if __name__ == "__main__":
    # Example: target your log directory or /tmp
    rotate_and_clean_logs(target_dir="/tmp", max_age_days=1, retention_days=14)

