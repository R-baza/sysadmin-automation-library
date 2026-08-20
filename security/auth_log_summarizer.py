from collections import defaultdict
import re

target = "/var/log/auth.log.1"
event_summary = defaultdict(lambda: defaultdict(int))

with open(target, "r") as f:
    for line in f:
        match = re.search(r"(\w+)\[(\d+)\]: (.*)", line)
        if match:
            process = match.group(1)
            message = match.group(3).strip()
            event_summary[process][message] += 1

with open("error_auth_log_1.txt", "w") as f:
    for process, messages in event_summary.items():
        f.write(f"{process}: {dict(messages)}\n")
        f.write("\n")


    
        


