'''
- This program stores students data into a JSON file
- The program allows adding, deleting, and searching students
'''

from pathlib import Path
import json
import secrets
from dataclasses import dataclass
from dataclasses import field


while True:
    print('Even if the file does not exist yet, include "filename.json" at the end of the path')
    path = Path(input('Enter JSON file path: ')).expanduser().resolve()

    if path.is_dir():
        print(f'{path} is not a file')
        continue
    if path.suffix != '.json':
        print(f'{path} is not a JSON file')
        continue
    if not path.exists():
        with path.open('w') as f:
            f.write('[]')
        break

    print()         # Separator
    break


# Show all students
def print_students(path):
    with path.open('r', encoding='utf-8') as f:
        students = json.load(f)
        for student in students:
            print(student)


# Add a new student
def make_student():
    with path.open('r', encoding='utf-8') as f:
        students = json.load(f)

    new_student = dict()

    # Generate a random 8-number id
    while True:
        new_student['id'] = "".join(secrets.choice("0123456789") for _ in range(8))

        for student in students:
            if new_student['id'] == int(student['id']):
                continue

        break

    new_student['full_name'] = input('Full Name: ')
    new_student['age'] = input('Age: ')
    new_student['year'] = input('Year: ')
    new_student['subjects'] = ''.join(input('Subjects (separated by commas): ').strip()).split(',')
    new_student['passed'] = input('Passed (t --> true | f --> false): ').lower()

    return new_student

def add_student(path, new_student):
    with path.open('a', newline='', encoding='utf-8') as f:
        json.dump(new_student, f)

new_student = make_student()
add_student(path, new_student)

# Fix TypeError: string indices must be integers, not 'str' in ine 52 --> student['id'] --> causing the problem

# Remove an existing student

# Search students