"""
Network Port Traffic Prioritization Engine

Description:
    A network automation logic module that classifies incoming connections 
    and determines queue priorities based on standard protocol port assignments 
    (e.g., HTTP/HTTPS, SSH, DNS). Mimics basic router Quality of Service (QoS) rules.

Author: Rodrigo Baza
"""
def route_traffic(port):
    if port == 80 or port == 443:
        return "Web traffic (High Priority)"
    elif port == 22 or port == 23:
        return "Management Traffic (Restricted Access)"
    elif port == 53:
        return "DNS Traffic (System Priority)"
    else:
        return "Standard Traffic (Low Priority)"
    
print(route_traffic(80))  # Example usage