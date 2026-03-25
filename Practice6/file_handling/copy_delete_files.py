import os
import shutil
from pathlib import Path

#-----------------------------------------------

# Create path objects
src_path = Path("files.txt")
dest_path = Path("backup.txt")

# 1. Check existence and type
if src_path.is_file():
    # 2. Modern way to read/write without manual 'with open' 
    # (Great for small text files)
    content = src_path.read_text()
    dest_path.write_text(content)
    
    # 3. Deleting
    dest_path.unlink() # This is the pathlib version of os.remove(), os.unlink()
    print("Backup file deleted.")
else:
    print("File not found.")

#-----------------------------------------------

source = "files.txt" # original
destination = "backup.txt" # copy

#basic copying
if os.path.exists(source) and os.path.isfile(source):
    with open(source, "rb") as fsrc: # read binary
        with open(destination, "wb") as fdst: # write binary
            fdst.write(fsrc.read()) # (over)write what you read
else:
    print("Source file does not exist")

if os.path.exists(destination): # you better check if it exist
    os.remove(destination) # for better error handling

#-----------------------------------------------

#Copying shutil: This copies the file AND its permissions(metadata, but sometimes not all)
if os.path.exists(source):
    shutil.copy2(source, destination) # copy2 preserves creation/modification dates
    print(f"Copied {source} to {destination}")

#-----------------------------------------------

if os.path.exists(destination): # Lets delete backup file
    os.remove(destination)