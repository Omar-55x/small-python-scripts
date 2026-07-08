"""
- Given a CSV file containing numeric data, this program will generate a summary for it

- For this use case, the CSV file will have to contain the fields: Name and Sales
- Output will be:
    1) Total records
    2) Total sales
    3) Average sales
    4) Best seller
    5) Worst seller
"""

from pathlib import Path
import csv
from dataclasses import dataclass


REQUIRED_FIELDS = {"Name", "Sales"}

@dataclass
class Results:
    records_count: int
    total_sales: int
    avg_sales: float
    best_seller: str
    worst_seller: str

def validate_path(prompt):
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

def make_analysis(path):
    with path.open('r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        if not REQUIRED_FIELDS.issubset(csv_reader.fieldnames):
            raise ValueError('CSV must contain Name and Sales fields')
        
        records_count = 0
        total_sales = 0

        highest_sale, lowest_sale = -1, float('inf')        # Highest and lowest sale
        best_seller, worst_seller = None, None          # Actual best and worst seller

        for row in csv_reader:
            sales = int(row['Sales'])

            records_count += 1
            total_sales += sales

            if sales > highest_sale:
                highest_sale = sales
                best_seller = row['Name']
            if sales < lowest_sale:
                lowest_sale = sales
                worst_seller = row['Name']

        if records_count == 0:
            raise ValueError('The CSV file contains no records')

        avg_sales = round(total_sales / records_count, 2)
    
    return Results(
        records_count=records_count,
        total_sales=total_sales,
        avg_sales=avg_sales,
        best_seller=best_seller,
        worst_seller=worst_seller
    )

def main():
    path = validate_path('Enter file path: ')
    try:
        results = make_analysis(path)
    except ValueError as e:
        print(e)
        return

    print(f'Number of records: {results.records_count}')
    print(f'Total sales: {results.total_sales}$')
    print(f'Average sales: {results.avg_sales}$')
    print(f'Best seller: {results.best_seller}')
    print(f'Worst seller: {results.worst_seller}')


if __name__ == '__main__':
    main()