import re


regex_id = r":(\d+)\)"
regex_error = r"DENIED"


with open("/var/log/syslog", "r") as infile, open("ssh_audit.txt", "a") as outfile:
    for line in infile:
        result = re.search(regex_id, line)
        final = re.search(regex_error, line)

       
        if result and final:
            log_entry = f"User ID: {result.group(1)}, Error: {final.group(0)}"
            print(log_entry)

            outfile.write(log_entry + "\n")
            


