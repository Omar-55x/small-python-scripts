"""
A program that copies image files from a directory into a directory called 'Img'

Img directory will be located at the user folder
Names of the files that were copied will be printed out
"""

from pathlib import Path
import shutil, sys



def organize_images(path):
    dest = Path(f'~/Img').expanduser()
    if not dest.exists():
        dest.mkdir()
    
    Image_suffixes = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.eps'}
    dest_names = [f.name for f in dest.iterdir()]
    for file in path.iterdir():
        if file.is_file():
            if file.suffix.lower() in Image_suffixes and file.name not in dest_names:
                try:
                    shutil.copy(file, dest)
                    print('Copied', file.name)
                except Exception as e:                                  # when file is locked or permission is denied
                    print(f'Failed to copy {file.name}: {e}')

def main():
    path = Path(input('Enter source directory path: '))

    if not path.exists() or not path.is_dir():
        print('Invalid Path')
        sys.exit()

    organize_images(path)


if __name__ == '__main__':
    main()