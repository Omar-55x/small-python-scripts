"""
- Given a CSV file, this program will read it and write a new CSV file with rows that specify a specific condition

- In this case we will filter products to include only products that has sold more than the average of total sales
- Required fields: Product, Sales
"""

from pathlib import Path
import csv


REQUIRED_FIELDS = ('Product', 'Sales')


while True:
    path = Path(input('Enter file path: ')).expanduser().resolve()

    if not path.exists():
        print(f'"{path}" does not exist')
        continue
    if not path.is_file():
        print(f'"{path}" is not a file')
        continue
    if path.suffix != '.csv':
        print('The file is not a CSV file')
        continue
    
    break

with path.open('r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    if not set(REQUIRED_FIELDS).issubset(csv_reader.fieldnames):
        raise ValueError('CSV must contain Product and Sales fields')

    records_count, total_sales = 0, 0
    for row in csv_reader:
        records_count += 1
        total_sales += int(row['Sales'])
    
    if records_count == 0:
        raise ValueError('The CSV contains no records')

    avg_sales = total_sales / records_count
    file.seek(0)
    csv_reader = csv.DictReader(file)

    with path.parent.joinpath('Best sellers.csv').open('w', newline='', encoding='utf-8') as new_file:
        csv_writer = csv.DictWriter(new_file, fieldnames=REQUIRED_FIELDS)

        csv_writer.writeheader()
        for row in csv_reader:
            if int(row['Sales']) > avg_sales:
                csv_writer.writerow(row)

        print('File has been created successfully')