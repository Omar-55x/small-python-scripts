"""
- Given a source directory, this program will organize the files into folders based on extension in these categories:
1) Images     2) Documents     3) Videos     4) Archives     5) Others

- To run the program from the terminal enter: py (python3 for macOS/Linux) mini_file_organizer.py "{path}"
"""

from pathlib import Path
import shutil
import argparse


CATEGORY_DIRS = [
    "Images",
    "Documents",
    "Videos",
    "Archives",
    "Others",
]

EXTENSIONS = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",

    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    ".mp4": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
}


# Make category directories
def make_dirs(path):
    for category in CATEGORY_DIRS:
        if not path.joinpath(category).exists():
            path.joinpath(category).mkdir()

# Get paths for all files
def gather_files(path):
    return [p for p in path.iterdir() if p.is_file()]

# Move files to the right directory based on its extension
def move_files(files, path):
    for file in files:
        extension = file.suffix.lower()
        category = EXTENSIONS.get(extension, 'Others')
        dest = path / category / file.name

        if dest.exists():
            handle_duplicates(file, dest)
        else:
            shutil.move(file, dest)

# Handle cases when a file with the same name already exists in the destination
def handle_duplicates(file_path, dest):
    uniq = 1

    while dest.exists():
        dest = dest.with_name(f'{file_path.stem}_{uniq}{dest.suffix}')
        uniq += 1

    file_path.rename(dest)

def main():
    parser = argparse.ArgumentParser(
        description='Organize files in folders based on the file extensions'
    )

    parser.add_argument('path', metavar='path', type=Path, help='The path of the folders to organize its files')
    args = parser.parse_args()
    path = args.path.expanduser().resolve()
    
    if not path.exists():
        parser.error(f'{path} does not exist')
    if not path.is_dir():
        parser.error(f'{path} is not a folder')

    make_dirs(path)
    files = gather_files(path)
    move_files(files, path)


if __name__ == '__main__':
    main()