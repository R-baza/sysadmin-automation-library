
import os 
import subprocess
import sys




if len(sys.argv) > 1:
    flag = sys.argv[1]
    
    if flag == "--disk":
        print("Running disk check...")
       
        subprocess.run(["df", "-h"])


    elif flag == "--uptime":
        print("Running uptime check...")
        uptime = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
        print(uptime.stdout)
       
        
    elif flag == "--memory":
        print("Running memory check...")
        subprocess.run(["free", "-m"])
    
    elif flag == "--all":
        print("Running all checks...")
        subprocess.run(["df", "-h"])
        subprocess.run(["uptime", "-p"])
        subprocess.run(["free", "-m"])
     
else:
    print("Please provide a flag, like --disk or --memory")


