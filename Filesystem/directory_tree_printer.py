"""
A program that prints the directory tree of the given directory
"""

from pathlib import Path
import sys


INDENT = '    '


def print_tree(path, indent):
    for p in path.iterdir():
        if p.is_file():
            print(f'{indent}{p.name}')
        else:
            print(f'{indent}{p.name}/')
            new_indent= indent + INDENT
            print_tree(p, new_indent)

def main():
    path = Path(input('Enter Directory Path: ')).expanduser()
    if not path.exists() or not path.is_dir():
        print('Invalid Directory')
        sys.exit()
    
    print(f'{path.name}/')
    print_tree(path, INDENT)


if __name__ == '__main__':
    main()