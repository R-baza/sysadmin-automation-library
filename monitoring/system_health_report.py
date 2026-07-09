"""
health_report.py

What it does: 
Programmatically parses raw system metric logs, calculates percentage-based 
storage utilization across multiple servers, and generates a structured 
environment health report with automatic threshold warnings.

Core Logic: 
File stream tokenization, type-casting data strings, mathematical formula 
logic, and conditional string reporting.

Author: Rodrigo Baza
"""

def check_storage(used_gb, total_gb):
    percentage = (used_gb / total_gb) * 100
    if percentage >= 85:
        return f"Warning: Storage usage is at {percentage:.2f}%"
    else:
        return f"Storage usage is at {percentage:.2f}%"

def generate_health_report(log_filepath="server_metrics.log", report_filepath="health_report.txt"):
    try:
        with open(log_filepath, "r") as file, open(report_filepath, "w") as output_file:
            for line in file:
                # Strip whitespace and split by comma CSV format
                parts = line.strip().split(",") 
                
                # Ensure the line has the expected data structure before unpacking
                if len(parts) == 3:
                    server_name = parts[0]
                    used = int(parts[1])
                    total = int(parts[2])
                    
                    status = check_storage(used, total)
                    output_file.write(f"{server_name}: {status}\n")
                    
        print(f"[SUCCESS] Health report generated successfully at '{report_filepath}'.")
        
    except FileNotFoundError:
        print(f"[ERROR] The metrics log file '{log_filepath}' could not be found.")
    except ValueError:
        print(f"[ERROR] Found invalid or corrupted numerical data inside '{log_filepath}'.")

if __name__ == "__main__":
    generate_health_report()


