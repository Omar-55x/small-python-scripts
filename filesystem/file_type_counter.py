"""
A program that counts how many files exist for each extension in a directory
"""

from pathlib import Path
import sys
from collections import Counter


def count_ext(path):
    counter = Counter()
    for file in path.iterdir():
        if file.is_file():
            ext = file.suffix.lower() or '[no extension]'
            counter[ext] += 1
    return counter

def main():
    path = Path(input('Enter full directory path: '))

    if not path.exists() or not path.is_dir():
        print('Invalid Directory')
        sys.exit()
    
    counter = count_ext(path)

    for ext, count in counter.most_common():           # Sorted by frequency
        print(f'{ext}: {count}')


if __name__ == '__main__':
    main()