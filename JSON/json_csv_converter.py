"""
- This program converts CSV files to JSON files and vice versa
- The conversion depends on the type of file you enter the path for
    - If CSV --> Output: JSON
    - If JSON --> Output: CSV

- Note: this program currently does not support nested JSON structure
    - It assumes the structure is as follows:
        [
            {
                key1:value1,
                key2:value2,
                ...
            },
            {
                ...
            },
            ...
        ]
"""

from pathlib import Path
import csv
import json


while True:
    path = Path(input('Enter CSV or JSON file Path: ').strip()).expanduser().resolve()

    if not path.exists():
        print(f'{path} does not exist')
        continue
    if not path.is_file():
        print(f'{path} is not a file')
        continue
    if path.suffix.lower() != '.csv' and path.suffix.lower() != '.json':
        print('File is not a CSV or a JSON file')
        continue

    break

if path.suffix == '.csv':
    with path.open('r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data =list(csv_reader)

        with path.with_suffix('.json').open('w', newline='', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
        
    print('CSV file has been converted successfully')

if path.suffix == '.json':
    with path.open('r', encoding='utf-8') as json_file:

        try:
            data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f'Invalid JSON: {e}')
            raise SystemExit

        if not data:
            print('JSON file is empty')
            raise SystemExit

        with path.with_suffix('.csv').open('w', newline='', encoding='utf-8') as csv_file:
            fieldnames = data[0].keys()
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            csv_writer.writeheader()
            for row in data:
                csv_writer.writerow(row)
    
    print('JSON file has been converted successfully')