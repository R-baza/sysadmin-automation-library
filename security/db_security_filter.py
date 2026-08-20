"""
db_security_filter.py

Description:
A lightweight Python utility designed to parse network firewall logs, 
isolate denied access attempts targeted at database servers, and export 
high-priority incidents to a dedicated security alerts file for rapid review.
"""
def extract_db_alerts(log_filepath="firewall.log", output_filepath="security_alerts.txt"):
    try:
        with open(log_filepath, "r") as file, open(output_filepath, "w") as output_file:
            alert_count = 0
            for line in file:
                if "DENY" in line and "DB_SERVER" in line:
                    output_file.write(line)
                    alert_count += 1
        print(f"[SUCCESS] Parsing complete. {alert_count} critical alerts written to '{output_filepath}'.")

    except FileNotFoundError:
        print(f"[ERROR] The log file '{log_filepath}' could not be found.")
if __name__ == "__main__":
    extract_db_alerts()
               