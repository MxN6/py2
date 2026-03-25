import os
import shutil
from pathlib import Path

# --- 1. Creating Nested Directories (Directory exercise 1) ---
base_dir = Path("Practice_Folder")
nested_path = base_dir / "reports" / "2024" / "logs"

# parents=True: creates all missing folders in the middle
# exist_ok=True: doesn't crash if the folder is already there
nested_path.mkdir(parents=True, exist_ok=True)
print(f"Directory structure created: {nested_path}")


# --- 2. Creating dummy files for testing (Preparation) ---
(base_dir / "readme.txt").write_text("Main info")
(nested_path / "system.log").write_text("All systems go")
(nested_path / "error.log").write_text("Error at 12:00")
(nested_path / "data.csv").write_text("id,name\n1,test")


# --- 3. Listing files and folders (Directory exercise 2) ---
print("\nContents of base directory (using os.listdir):")
# os.listdir() returns a list of strings
for item in os.listdir(base_dir):
    print(f"- {item}")


# --- 4. Finding files by extension (Directory exercise 3) ---
print("\nFinding all .log files recursively (using pathlib):")
# rglob stands for "recursive glob"
log_files = list(base_dir.rglob("*.log"))

for log in log_files:
    # .name gives just the filename, .parent gives the folder path
    print(f"Found log: {log.name} in {log.parent}")


# --- 5. Clean up / Management (using shutil) ---
# If you wanted to delete the entire directory tree safely:
shutil.rmtree(base_dir) 
print(f"\nSuccessfully removed {base_dir} and all its contents.")