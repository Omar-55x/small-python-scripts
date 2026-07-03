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
    for dir in CATEGORY_DIRS:
        if not path.joinpath(dir).exists():
            path.joinpath(dir).mkdir()

# Get paths for all files
def gather_files(path):
    files = [p for p in path.iterdir() if p.is_file()]
    return files

# Move files to the right directory based on its extension
def move_files(files, path):
    for file in files:
        match file.suffix.lower():
            case '.pdf' | '.doc' | '.docx' | '.txt' | '.ppt' | '.pptx' | '.xls' | '.xlsx':
                dest = path / 'Documents' / file.name
            case '.jpg' | '.png' | '.gif' | '.jpeg' | '.webp':
                dest = path / 'Images' / file.name
            case '.mp4' | '.mkv' | '.avi' | '.mov':
                dest = path / 'Videos' / file.name
            case '.zip' | '.rar' | '.7z' | '.tar' | '.gz':
                dest = path / 'Archives' / file.name
            case _:
                dest = path / 'Others' / file.name

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