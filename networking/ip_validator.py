"""
Network Infrastructure IP Address Validator

Description:
    A core network engineering utility designed to parse and validate IPv4 string structures. 
    Ensures input strings match standard dot-decimal notation thresholds (0-255 per octet)[cite: 2] 
    before committing configurations to network interfaces, routers, or firewall access control lists (ACLs).

Author: Rodrigo Baza
"""
def is_valid_ipv4(ip_string):
    parts = ip_string.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        number = int(part)
        if number < 0 or number > 255:
            return False
    return True

print(is_valid_ipv4("192.168.1.1"))