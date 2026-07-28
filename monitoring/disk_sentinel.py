import shutil
import time 
import os   
remove_files = []
disk_usage = shutil.disk_usage("/")
files = os.path.join("/", "var", "log", "auth.log.1")
if disk_usage.free < 0.2 * disk_usage.total:
    if files:
        if os.path.getmtime(files) < time.time() - 86400:
            try:
                remove_files.append(files)
                print(f"Added to removal list: {files}")
            except Exception as e:
                print(f"Error adding to removal list: {e}")



   



