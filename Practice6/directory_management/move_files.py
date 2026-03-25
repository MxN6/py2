import shutil
from pathlib import Path

# 1. Define source and destination
base_dir = Path("Practice_Folder")
archive_dir = base_dir / "archive"

# 2. Ensure the destination directory exists
# parents=True creates intermediate folders if they don't exist
archive_dir.mkdir(parents=True, exist_ok=True)

# 3. Find and Move files
print("Moving files...")

# We use rglob to find all .log files in any subfolder
for file_path in base_dir.rglob("*.log"):
    # Define the new path (same filename, but inside the archive folder)
    destination = archive_dir / file_path.name
    
    # shutil.move handles the actual "cut and paste"
    shutil.move(str(file_path), str(destination))
    
    print(f"Moved: {file_path.name} -> {archive_dir}")

print("\nMove operation complete.")