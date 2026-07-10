"""
- Given a CSV file of students names and grades, this program will make a report for their grades
- Constraints: the field names should be only 'Name' for names and subjects names

- Output:
    1) Each student name, their average grade, and status
    2) Class's average grade, the students with the highest and lowest average
"""

from pathlib import Path
from dataclasses import dataclass, field
import csv


@dataclass
class Student:
    name: str
    grades: dict[str, float]
    avg_grade: float = field(init=False)
    status: str = field(init=False)

    # The following functions run automatically after initialization
    def __post_init__(self):
        self.avg_grade = self.calc_avg()
        self.status = self.check_status()

    def calc_avg(self) -> float:
        total_grade = sum(self.grades.values())
        return round(total_grade / len(self.grades), 2)
    
    def check_status(self) -> str:
        fail_list = [subject for subject, grade in self.grades.items() if grade < 60]
        
        if not fail_list:
            return 'Pass'
        else:
            return f"Fail at {', '.join(fail_list)}"
        

# Path validation
def validate_path(prompt) -> Path:

    while True:
        path = Path(input(prompt)).expanduser().resolve()

        if not path.exists():
            print(f'"{path}" does not exist')
            continue
        if not path.is_file():
            print(f'"{path}" is not a file')
            continue
        if path.suffix != '.csv':
            print('The file is not a CSV file')
            continue

        return path


# Gather all students info into students objects
def gather_students(path: Path) -> list[Student]:

    students = []

    with path.open('r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        if 'Name' not in csv_reader.fieldnames:
            raise ValueError('\'Name\' field does not exist')

        for row in csv_reader:
            stud_name = row['Name']
            stud_grades = {k:float(v) for k, v in row.items() if k != 'Name'}

            students.append(Student(
                name=stud_name,
                grades=stud_grades
            ))
    
    return students


# Calculate class avg, highest and lowest
def make_class_summary(students: list[Student]) -> dict:

    total_avg = sum(stud.avg_grade for stud in students)
    class_avg = round(total_avg / len(students), 2)

    # Students with the highest and lowest grades
    highest = max(students, key=lambda s: s.avg_grade)
    lowest = min(students, key=lambda s: s.avg_grade)

    return {
        'class_avg': class_avg,
        'highest': highest.name,
        'highest_avg': highest.avg_grade,
        'lowest': lowest.name,
        'lowest_avg': lowest.avg_grade
    }


# Write grades report
def make_report(report_path: Path, students: list[Student], class_summary: dict):

    with report_path.open('w', encoding='utf-8') as f:
        f.write('Student Report\n\n')
        f.write('====================\n\n')

        # Write students report
        for stud in students:
            f.write(f'''{stud.name}
Average: {stud.avg_grade}
Status: {stud.status}\n\n''')
            
        f.write('--------------------\n\n')

        # Write class summary
        f.write(f'''Class Average: {class_summary['class_avg']}
Highest Average: {class_summary['highest']} ({class_summary['highest_avg']})
Lowest Average: {class_summary['lowest']} ({class_summary['lowest_avg']})''')


def main():

    path = validate_path('Enter file path: ')

    try:
        students = gather_students(path)

        if not students:
            print('No students found')
            return
    except ValueError as e:
        print(e)
        return
    
    class_summary = make_class_summary(students)
    report_path = path.parent.joinpath('Grades Report.txt')
    make_report(report_path, students, class_summary)


if __name__ == '__main__':
    main()