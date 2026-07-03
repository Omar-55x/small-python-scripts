"""
Given a source directory, this program will organize the files into folders based on extension in these categories:
1) Images     2) Documents     3) Videos     4) Archives     5) Others
"""

from pathlib import Path
import shutil


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

def validate_path(prompt):
    while True:
        path = Path(input(prompt)).expanduser().resolve()

        if not path.exists():
            print(f'"{path}" does not exist')
            continue
        if not path.is_dir():
            print(f'"{path}" is not a directory')
            continue
        return path

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
        catergory = EXTENSIONS.get(extension, 'Others')
        dest = path / catergory / file.name

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
    path = validate_path('Enter folder path: ')
    make_dirs(path)
    files = gather_files(path)
    move_files(files, path)


if __name__ == '__main__':
    main()