import re


auth_log = "/var/log/auth.log"
failed_attempts = {}
with open(auth_log, "r") as f:
    for line in f:
        if re.search(r"authentication failure", line):
            attempt = re.search(r"rhost=(\S+)", line)
            if attempt:
                failed_attempts[attempt.group(1)] = failed_attempts.get(attempt.group(1), 0) + 1

for attempt, count in failed_attempts.items():
    print(f"Attempt {attempt}: {count} failed attempts")

        
