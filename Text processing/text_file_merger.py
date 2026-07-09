"""
- Given a directory containing multiple ".txt" files, this program will merge them alphabetically into one ".txt" file

- The file will be saved as "merged.txt" in the same directory
- Empty files are not added to "merged.txt"
"""

from pathlib import Path


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

def gather_files(path):
    files = [
        p for p in path.iterdir()
        if p.suffix == '.txt' and p.name != 'merged.txt'
    ]

    return sorted(files, key=lambda p: p.name.lower())      # To make sorting case-insensitive

def merge_files(merged_path, files):
    with merged_path.open('w', newline='', encoding='utf-8') as merged_file:
        for file in files:
            if file.stat().st_size == 0:       # Check if file is empty
                continue
            
            with file.open('r', encoding='utf-8') as f:
                merged_file.write(f'====== {file.name} ======\n\n')

                for line in f:
                    merged_file.write(line)
                merged_file.write('\n\n')

def main():
    path = validate_path('Enter directory path: ')
    files = gather_files(path)
    
    if not files:
        print('No text files found')
        return
    
    merged_path = path / 'merged.txt'
    merge_files(merged_path, files)


if __name__ == '__main__':
    main()