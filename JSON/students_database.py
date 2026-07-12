'''
- This program stores students data into a JSON file
- The program allows adding, deleting, and searching students

- How to run the program:
    - Enter a valid path including file name and .json extension (if it does not exist, a file with that name will be created)
    - Enter the number of the operation you want to perform [1-4]
    - Follow along with the requirements
    - Enter 'q' or 'Q' to exit the program
'''

from pathlib import Path
import json
import secrets


def validate_path(prompt):
    while True:
        print('Even if the file does not exist yet, include "filename.json" at the end of the path')
        path = Path(input(prompt)).expanduser().resolve()

        if path.is_dir():
            print(f'{path} is not a file')
            continue
        if path.suffix != '.json':
            print(f'{path} is not a JSON file')
            continue
        if not path.exists():
            with path.open('w', encoding='utf-8') as f:
                json.dump([], f)
            break

        print()
        break

    return path


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

# Helper functions
def load_students(path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
    
def save_students(path, students):
    with path.open('w', newline='', encoding='utf-8') as f:
        json.dump(students, f, indent=4)

def print_info(student):
    print(f'''Name: {student['full_name']}
Age: {student['age']}
Year: {student['year']}
Subjects: {', '.join(student['subjects'])}
Status: {'Passed' if student['passed'] == True else 'Failed'}\n''')


# Print all students
def print_students(path):
    students = load_students(path)

    if not students:
        print("No students in the database")
        return

    for student in students:
        print_info(student)
        print('---------------- \n')
        

# Make a new student Python dict --> JSON object
def make_student(path):
    students = load_students(path)
    new_student = {}

    # Generate a random 8-number id
    while True:
        new_student['student_id'] = "".join(secrets.choice("0123456789") for _ in range(8))

        if not any(new_student['student_id'] == student['student_id'] for student in students):
            break

    new_student['full_name'] = input('Full Name: ')
    new_student['age'] = input('Age: ')
    new_student['year'] = input('Year: ')
    new_student['subjects'] = ''.join(input('Subjects (separated by commas): ').strip().split()).split(',')     # Also removes spaces in between subjects
    passed = input('Passed? (t --> true | f --> false): ').lower()
    
    if passed in ('t', 'true', 'y', 'yes'):
        new_student['passed'] = True
    elif passed in ('f', 'false', 'n', 'no'):
        new_student['passed'] = False
    else:
        passed = None

    return new_student

# Add the new student to the database
def add_student(path, new_student):
    students = load_students(path)
    students.append(new_student)
    save_students(path, students)
    print(f'{new_student['full_name']} has been added to the database\n')


# Remove an existing student by ID
def remove_student(path):

    student_id = validate_id()
    students = load_students(path)
    
    for student in students:
        if student_id == int(student['student_id']):
            students.remove(student)
            save_students(path, students)

            print(f'{student['full_name']} has been removed from the database\n')
            return
    
    # If no matching ID found
    print('No student found with the given ID number\n')
    return

# Search for a student by ID
def search_student(path):

    student_id = validate_id()
    students = load_students(path)

    for student in students:
        if student_id == int(student['student_id']):
            print_info(student)
            return
    
    print('No student found with the given ID number')
    return

def main():

    path = validate_path('Enter JSON file path: ')

    print('''What operation do you want to perform?
1- Get all students
2- Search for a student by ID
3- Add a new student
4- Remove a student\n''')

    while True:
        command = input('Enter operation number (q to exit): ')
        print()

        match command:
            case '1':
                print_students(path)
            case '2':
                search_student(path)
            case '3':
                new_student = make_student(path)
                add_student(path, new_student)
            case '4':
                remove_student(path)
            case 'q' | 'Q':
                exit()
            case _:
                print('Invalid input\n')


main()