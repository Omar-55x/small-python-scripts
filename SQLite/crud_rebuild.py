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



def validate_id():
    while True:

        try:
            student_id = int(input('Please provide student\'s ID number: '))
        except ValueError:
            print('ID has to be a number')
            continue

        if len(str(student_id)) != 8:
            print('ID has to consist of 8 numbers')
            continue
    
        return student_id


# student info validators
def get_valid_name():
    while True:
        full_name = input('Full Name: ').strip()

        if not full_name:
            print('Name can not be empty')
            continue
        if not all(char.isalpha() or char.isspace() for char in full_name):
            print('Name can not contain non-alphabetical characters')
            continue

        return full_name
    
def get_valid_age():
    while True:
        try:
            age = int(input('Age: ').strip())
            if age < 0:
                print('Age can not be negative')
                continue
        except ValueError:
            print('Age has to be a number')
            continue

        return age
    
def get_valid_grade():
    while True:
        grade = int(input('Grade number: ').strip())

        if not grade:
            print('Grade can not be empty')
            continue
        if grade > 12 or grade < 1:
            print('Grade has to be a number from 1 to 12')
            continue

        return grade

def get_valid_subjects():
    while True:
        subjects = input('Subjects (separated by commas): ').strip()
        subjects_list = ''.join(subjects.split()).split(',')     # split() --> split(',') removes spaces in between subjects

        if not subjects:
            print('Subjects can not be empty')
            continue

        valid = True

        for subject in subjects_list:
            if not subject.isalpha():
                print('Subejcts can not contain non-alphabetical characters')
                valid = False
                continue
        
        if not valid:
            continue
        
        return subjects_list
    
def get_valid_status():
    while True:
        status = input('Status? (t/true --> passed | f/false --> failed): ').strip().lower()

        if status in ('t', 'true', 'y', 'yes'):
            return 'Passed'
        elif status in ('f', 'false', 'n', 'no'):
            return 'Failed'
        else:
            print('Please enter a valid status')
            continue


# Helper function
def print_info(student, subjects):
    print(f'''Name: {student[1]}
Age: {student[2]}
Grade: {student[3]}
Subjects: {', '.join(subject[0] for subject in subjects)}
Status: {student[4]}\n''')
    

def print_students(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute("SELECT subject FROM students_subjects WHERE student_id = ?", (row[0],))
            subjects = cursor.fetchall()

            print(row)
            print('Subjects:', ', '.join(subject[0] for subject in subjects))
            print()

        logging.info('Displayed all students')


def make_student(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT student_id FROM students')
        studnets_ids = {row[0] for row in cursor.fetchall()}

    new_student = {}

    # Generate a random 8-number id
    while True:
        new_student['student_id'] = int("".join(secrets.choice("0123456789") for _ in range(8)))

        if len(str(new_student['student_id'])) != 8:        # for cases starting with 0 that will end up as 7-digit id
            continue

        if new_student['student_id'] not in studnets_ids:
            break

    new_student['full_name'] = get_valid_name()
    new_student['age'] = get_valid_age()
    new_student['grade'] = get_valid_grade()
    new_student['subjects'] = get_valid_subjects()
    new_student['status'] = get_valid_status()

    return new_student


# Add the new student to the database
def add_student(conn, new_student):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO students
            (student_id, full_name, age, grade, status)
            VALUES
            (?, ?, ?, ?, ?);""",
            (new_student['student_id'], new_student['full_name'], new_student['age'], new_student['grade'], new_student['status'])
        )

        for subject in new_student['subjects']:
            c.execute("INSERT INTO students_subjects (student_id, subject) VALUES (?, ?);",
                (new_student['student_id'], subject)
            )

    logging.info('Added student %s (%s)', new_student['full_name'], new_student['student_id'])
    print(f'{new_student['full_name']} has been added to the database\n')


# Search student by ID
def search_student(conn):
    student_id = validate_id()

    with conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()

        cursor.execute("SELECT subject FROM students_subjects WHERE student_id = ?", (student_id,))
        subjects = cursor.fetchall()

        logging.info('Displayed student %s (%s)', student[1], student[0])
        print()
        print_info(student, subjects)
        return

    logging.warning('Student lookup failed. ID: %s does not exist', student_id)
    print('No student found with the given ID number')
    return


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
        with conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade INTEGER NOT NULL,
            status TEXT
            );""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS students_subjects (
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
            );""")
    except sqlite3.OperationalError:
        logging.exception('Operational Error')
        print('An operational error occured. Check logs for more information.')
        return

    logging.info('Connected to the database at: %s', data_file)

    print()
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
                        logging.exception('Non-identified error')
                        raise
            case '2':
                search_student(conn)
            case '3':
                new_student = make_student(conn)
                add_student(conn, new_student)
            case 'q' | 'Q':
                logging.info('Program terminated')
                conn.close()
                exit()
            case _:
                print('Invalid input\n')


main()