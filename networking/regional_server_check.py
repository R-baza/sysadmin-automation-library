"""
Multi-Region Infrastructure Storage Audit

Description:
    A localized infrastructure monitoring script that categorizes system assets 
    by global operational regions (e.g., Singapore, London). Iterates through 
    regional hardware metrics to isolate storage saturation anomalies.

Author: Rodrigo Baza
"""
singapore_servers = {"web-01": 90, "db-01": 40,}
london_servers = {"web-02": 15, "db-02": 88}

def check_regional_disk(server_dictionary):
    for name, percentage in server_dictionary.items():
        if percentage >= 85:
            print(f"[WARNING] Server {name} is critically full at {percentage}%!")
        else:
            print(f"[OK] Server {name} is healthy at {percentage}")


print("--- Checking Singapore ---")
check_regional_disk(singapore_servers)

print("\n--- Checking London ---")
check_regional_disk(london_servers)



