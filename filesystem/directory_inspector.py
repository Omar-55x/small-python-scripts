"""
A program that takes a directory path (not recursively) and returns:
1) Number of files
2) Number of folders
3) Total size of all files
4) Largest file
5) Smallest file
"""

from pathlib import Path
import sys


path = Path(input("Enter full path: "))

if not path.exists() or not path.is_dir():
    print('Invalid Directory')
    sys.exit()

# Find requirements
file_count, folder_count, total_size = 0, 0, 0
largest, smallest = None, None
for p in path.iterdir():
    if p.is_file():
        file_count += 1
        total_size += p.stat().st_size

        if largest is None or p.stat().st_size > largest.stat().st_size:
            largest = p

        if smallest is None or p.stat().st_size < smallest.stat().st_size:
            smallest = p
    else:
        folder_count += 1

# For human readable size
for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
    if total_size < 1024:
        hr_size = f"{total_size:.2f} {unit}"
        break
    total_size /= 1024

print(f'Number of files: {file_count}')
print(f'Number of folders: {folder_count}')
print(f'Total size of files: {hr_size}')
print(f'Largest file: {largest.name}')
print(f'Smallest file: {smallest.name}')