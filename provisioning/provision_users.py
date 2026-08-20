#!/usr/bin/env python3
import subprocess


with open("new_hires.csv", "r") as f:
    content = f.read()
    for line in content.split("\n"):
        if line.strip():
           first_name, last_name, deparment = line.split(",")
           new_email = f"{first_name}.{last_name}@company.com"
           print(new_email)

           new_user = f"{first_name.lower()}.{last_name.lower()}"
           new_password = f"password123"
           print(new_user)
           useradd = f"useradd {new_user}"
           print(useradd)
           subprocess.run(useradd, shell=True)
           subprocess.run(f"groupadd {deparment}", shell=True)
           subprocess.run(f"usermod -aG {deparment} {new_user}", shell=True)
           subprocess.run(f"echo '{new_user}:{new_password}' | chpasswd", shell=True)
           try:
               subprocess.run(f"mkdir /home/{new_user}", shell=True)
           except Exception as e:
               print(f"Error creating home directory: {e}")

           with open("provisioning.log", "a") as outfile:
               outfile.write(f"User {new_user} created with email {new_email}\n")








        
        
