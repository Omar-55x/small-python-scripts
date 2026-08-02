'''
- Rebuilding the JSON > students_database.py script with SQLite functionality
- The version stores students data in a students.db file in a given folder path

- How to run the program:
    - In the terminal run: py/python3 crud_rebuild.py "folder path"
    - Enter the number of the operation you want to perform [1-5]
    - Follow along with the requirements
    - Enter 'q' or 'Q' to exit the program
'''

from pathlib import Path
import argparse
import sqlite3
import secrets
import logging



def print_students(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM IF EXISTS students")

        rows = cursor.fetchall()
        for row in rows:
            print(row)
        logging.info('Displayed all students')
        

def main():
    ''' Past-UI configuration and validations '''

    # Take and validate folder path
    parser = argparse.ArgumentParser(
        description='Store students data in a SQL database'
    )

    parser.add_argument('path', type=Path, help='Enter a valid folder path to store the data')
    args = parser.parse_args()

    path = args.path.expanduser().resolve()

    if not path.is_dir():
        parser.error(f'{path} is not an existing folder')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        filename=path / 'students.log',
        format='%(asctime)s  %(levelname)s:%(message)s'
    )

    logging.info('Program started')

    # Connect to the DB
    data_file = path / 'students.db'
    try:
        conn = sqlite3.connect(data_file)
    except sqlite3.OperationalError:
        logging.exception('Operational Error')
        print('An operational error occured. Check logs for more information.')
        return

    logging.info('Connected to the database at: %s', data_file)

    while True:
        print('''What operation do you want to perform?
1- Get all students
2- Search for a student by ID
3- Add a new student
4- Update student\'s info
5- Remove a student\n''')

        command = input('Enter operation number (q to exit): ')
        print()

        match command:
            case '1':
                try:
                    print_students(conn)
                except sqlite3.OperationalError as e:
                    if 'no such table' in str(e):
                        logging.warning('Table does not exist')
                        print('Students table does not exist. Please add students first.\n')
                    else:
                        logging.exception()
                        raise
            case 'q' | 'Q':
                logging.info('Program terminated')
                exit()
            case _:
                print('Invalid input\n')


main()