"""
Infrastructure SLA Uptime Calculator

Description:
    An operational metrics tool that calculates a service's monthly availability percentage 
    based on recorded downtime hours. Automatically checks performance metrics against a standard 
    enterprise 99.9% High Availability Service Level Agreement (SLA) threshold.

Author: Rodrigo Baza
"""
def calculate_uptime(downtime_hours):
    uptime_percentage = ((720 - downtime_hours) / 720) * 100
    if uptime_percentage < 99.9:
        return f"SLA Breach! Uptime is {uptime_percentage:.2f}%"
    else:
        return f"SLA OK! Uptime: {uptime_percentage}%"


#   Example Usage
if __name__ == "__main__":
    print("--- Ruunning Infrastructure SLA Status Checks ---")

    # Example 1: Minimal downtime (Within safe SLA limits)
    print(calculate_uptime(0.5)) # 30 minutes of downtime
    # Example 2: Major outage (Triggers an SLA breach)
    print(calculate_uptime(4.5)) # 4 and a half hours of downtime