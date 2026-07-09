"""
Infrastructure Server Inventory Tracker

Description:
    A system utility that parses infrastructure hostnames and leverages naming convention 
    patterns to isolate and count active production environments. Mimics dynamic inventory 
    filtering workflows found in automated configuration management pipelines.

Author: Rodrigo Baza
"""
servers = ["prod-web-01", "dev-db-01", "prod-email-02", "dev-test-01", "prod-db-03"]
prod_count = 0
for production in servers:
    # Check for the 'prod' naming convention flag in the hostname
    if "prod" in production:
        prod_count = prod_count + 1
print("Total production servers: ", prod_count)