"""
Log-Based System Availability Counter

Description:
    An event-driven status tracking utility that processes sequential system heartbeat logs.
    It analyzes historical state arrays ("UP" / "DOWN" pings) to calculate a cumulative 
    availability percentage, reflecting real-world log analysis workflows used in continuous monitoring.

Author: Rodrigo Baza
"""
def calculate_uptime(log_list):
    if len(log_list) == 0:
        return "0.0%"
    # Count occurrences of operational "UP" flags
    uptime_count = log_list.count("UP")
    uptime_percentage = uptime_count / len(log_list) * 100
    return f"{uptime_percentage:.1f}%"

my_log = ["UP", "DOWN", "UP", "UP", "DOWN", "UP"]

result = calculate_uptime(my_log)
print(result)

