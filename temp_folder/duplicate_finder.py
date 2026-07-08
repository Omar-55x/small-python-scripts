"""
A program that searches a directory recursively and reports files with the same name
"""

from pathlib import Path
import sys

# Collect and group files by filenames
def gather_files(path, files):
    for p in path.iterdir():
        if p.is_file():
            files.setdefault(p.name, []).append(p)
        if p.is_dir():
            gather_files(p, files)
    
# Report if duplicates are found
def report_duplicates(files):
    found = False

    for name, paths in files.items():
        if len(paths) > 1:
            found = True
            print(name)
            for path in paths:
                print(f'    {path}')
    
    if not found:
        print("No duplicates found")

def main():
    path = Path(input('Enter Directory Path: '))

    if not path.exists() or not path.is_dir():
        print('Invalid Directory')
        sys.exit()
    
    files = {}
    gather_files(path, files)
    report_duplicates(files)


if __name__ == '__main__':
    main()