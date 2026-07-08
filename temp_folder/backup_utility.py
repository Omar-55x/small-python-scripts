"""
A backup utility - given a source directory, this program will create a backup directory for it
"""

from pathlib import Path
import shutil
from datetime import datetime


# make sure path exists and is a directory
def validate_path(path):
    if not path.exists():
        raise FileNotFoundError(f'"{path}" does not exist')
    if not path.is_dir():
        raise NotADirectoryError(f'"{path}" is not a directory')

# if not a valid path --> raise exception --> reprompt the user
def get_directory(prompt):
    while True:
        path = Path(input(prompt)).expanduser().resolve()

        try:
            validate_path(path)
            return path
        except (FileNotFoundError, NotADirectoryError) as e:
            print(e)
            print('Please try again')

# create a backup with a timestamp
def create_backup(source, dest):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup = dest / f'{source.name}_backup_{timestamp}'
    shutil.copytree(source, backup)
    return backup

def main():
    source = get_directory('Source Directory Path: ')
    dest = get_directory('Path for Backup: ')

    try:
        backup = create_backup(source, dest)
        print(f'Backup created at: {backup.resolve()}')
    except Exception as e:
        print(f'Failed to create backup: {e}')
    
    

if __name__ == '__main__':
    main()