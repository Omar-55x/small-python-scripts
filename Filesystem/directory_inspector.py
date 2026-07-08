"""
A program that scans a directory path (not recursively) and returns:
1) Number of files
2) Number of folders
3) Total size of all files
4) Largest file
5) Smallest file
"""

from pathlib import Path
import sys
from dataclasses import dataclass

@dataclass
class InspectionResult:
    file_count: int
    folder_count: int
    total_size: int
    largest: Path | None
    smallest: Path | None

def inspect_directory(path):
    # Find information about the contents of a folder
    file_count, folder_count, total_size = 0, 0, 0
    largest, smallest = None, None
    largest_size, smallest_size = -1, float('inf')
    for p in path.iterdir():
        size = p.stat().st_size
        if p.is_file():
            file_count += 1
            total_size += size

            if largest is None or size > largest_size:
                largest = p
                largest_size = size

            if smallest is None or size < smallest_size:
                smallest = p
                smallest_size = size
        else:
            folder_count += 1
    
    return InspectionResult(
        file_count=file_count,
        folder_count=folder_count,
        total_size=total_size,
        largest=largest,
        smallest=smallest
    )

def human_readable_size(total_size):
    # Convert a size in bytes into a human-readable format
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if total_size < 1024:
            hr_size = f"{total_size:.2f} {unit}"
            return hr_size
        total_size /= 1024

def main():
    path = Path(input("Enter full path: "))

    if not path.exists() or not path.is_dir():
        print('Invalid Directory')
        sys.exit()

    result = inspect_directory(path)
    hr_size = human_readable_size(result.total_size)

    print(f'Number of files: {result.file_count}')
    print(f'Number of folders: {result.folder_count}')
    print(f'Total size of files: {hr_size}')
    if result.largest:
        print(f'Largest file: {result.largest.name}')
    else:
        print('Largest file: None')
    if result.smallest:
        print(f'Smallest file: {result.smallest.name}')
    else:
        print('Smallest file: None')


if __name__ == '__main__':
    main()