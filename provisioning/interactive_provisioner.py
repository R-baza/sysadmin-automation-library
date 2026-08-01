#!/usr/bin/env python3
import subprocess


first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
department = input("Enter department: ")

new_email = f"{first_name.lower()}.{last_name.lower()}@company.com"
print(new_email)

new_user = f"useradd {first_name.lower()}.{last_name.lower()}"
print(new_user)

subprocess.run(new_user, shell=True)

subprocess.run(f"groupadd {department}", shell=True)
subprocess.run(f"usermod -aG {department} {first_name.lower()}.{last_name.lower()}", shell=True)
subprocess.run(f"echo '{first_name.lower()}.{last_name.lower()}:password123' | chpasswd", shell=True)

try:
    subprocess.run(f"mkdir /home/{first_name.lower()}.{last_name.lower()}", shell=True)
except Exception as e:
    print(f"Error creating home directory: {e}")
    with open("provisioning.log", "a") as outfile:
        outfile.write(f"Error creating home directory for {first_name} {last_name}: {e}\n")


