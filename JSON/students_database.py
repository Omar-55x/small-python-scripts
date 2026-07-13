'''
- This program stores students data into a JSON file
- The program allows adding, updating, deleting, and searching students

- How to run the program:
    - Enter a valid path including file name and .json extension (if it does not exist, a file with that name will be created)
    - Enter the number of the operation you want to perform [1-5]
    - Follow along with the requirements
    - Enter 'q' or 'Q' to exit the program
'''

from pathlib import Path
import json
import secrets

# Path validator
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


# ID validator
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
    
# New student info validators
def get_valid_name():
    while True:
        full_name = input('Full Name: ')

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
            age = int(input('Age: '))
            if age < 0:
                print('Age can not be negative')
                continue
        except ValueError:
            print('Age has to be a number')
            continue

        if not age:
            print('Age can not be empty')
            continue

        return age
    
def get_valid_year():
    while True:
        year = input('Year: ')

        if not year:
            print('Year can not be empty')
            continue
        if not all(char.isalnum() or char.isspace() for char in year):
            print('Year can not contain non-alphanumeric characters')
            continue

        return year

def get_valid_subjects():
    while True:
        subjects = input('Subjects (separated by commas): ')
        subjects_list = ''.join(subjects.strip().split()).split(',')     # split() --> split(',') removes spaces in between subjects

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
    
def get_valid_bool():
    while True:
        passed = input('Passed? (t --> true | f --> false): ').lower()

        if passed in ('t', 'true', 'y', 'yes'):
            return True
        elif passed in ('f', 'false', 'n', 'no'):
            return False
        else:
            print('Please write a valid status')
            continue


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

    new_student['full_name'] = get_valid_name()
    new_student['age'] = get_valid_age()
    new_student['year'] = get_valid_year()
    new_student['subjects'] = get_valid_subjects()
    new_student['passed'] = get_valid_bool()

    return new_student


# Add the new student to the database
def add_student(path, new_student):
    students = load_students(path)
    students.append(new_student)
    save_students(path, students)
    print(f'{new_student['full_name']} has been added to the database\n')


# Update student's info
def update_student(path):
    student_id = validate_id()
    students = load_students(path)

    for student in students:
        if student_id == int(student['student_id']):
            while True:
                print()
                print(f'''What do you want to update for {student['full_name']}?
1- Name
2- Age
3- Year
4- Subjects
5- Passing status\n''')
                
                command = input('Enter operation number (q to exit): ')
                print()

                match command:
                    case '1':
                        student['full_name'] = get_valid_name()
                        save_students(path, students)
                    case '2':
                        student['age'] = get_valid_age()
                        save_students(path, students)
                    case '3':
                        student['year'] = get_valid_year()
                        save_students(path, students)
                    case '4':
                        student['subjects'] = get_valid_subjects()
                        save_students(path, students)
                    case '5':
                        student['passed'] = get_valid_bool()
                        save_students(path, students)
                    case 'q' | 'Q':
                        return
                    case _:
                        print('Invalid input\n')
    
    # If no matches are found
    print('No student found with the given ID number\n')
    return
    

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
                print_students(path)
            case '2':
                search_student(path)
            case '3':
                new_student = make_student(path)
                add_student(path, new_student)
            case '4':
                update_student(path)
            case '5':
                remove_student(path)
            case 'q' | 'Q':
                exit()
            case _:
                print('Invalid input\n')


main()