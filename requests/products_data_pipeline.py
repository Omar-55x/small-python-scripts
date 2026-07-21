'''
- A data pipeline that uses this workflow: API --> JSON --> Extract needed fields --> Save to CSV --> Write text summary

- In this case,
 the API will include information about different proudcts.
 The fields to extract are title, price, category, and rating.
 The summary will include:
   1- The average price and rating for each category.
   2- The products with the highest and lowest rating.
   3- The categories with the highest and lowest average rating.

- API used: https://dummyjson.com/products
'''

import requests
from pathlib import Path
import csv
from dataclasses import dataclass


@dataclass
class Results:
    highest_rating: dict
    lowest_rating: dict
    category_statistics: dict
    highest_category: str
    lowest_category: str

FIELD_NAMES = ('title', 'category', 'price', 'rating')
API_URL = 'https://dummyjson.com/products'


def fetch_products():
    products_response = requests.get(API_URL, timeout=10)
    products_response.raise_for_status()
    return products_response.json()['products']


def extract_fields(products):
    extracted_products = []

    for product in products:
        extracted_product = {field: product[field] for field in FIELD_NAMES}
        extracted_products.append(extracted_product)

    return extracted_products


def validate_path(prompt):
    while True:
        path = Path(input(prompt).strip()).resolve().expanduser()

        if not path.exists():
            print(f'{path} does not exist')
            continue
        if not path.is_dir():
            print(f'{path} is not a folder')
            continue

        return path


# Save products into a CSV file
def write_csv(path, extracted_products):
    csv_path = path / 'products.csv'

    with csv_path.open('w', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()

        for product in extracted_products:
            csv_writer.writerow(product)


def calc_statistics(extracted_products):
    category_statistics = {}

    highest_rating = max(extracted_products, key=lambda p: p['rating'])
    lowest_rating = min(extracted_products, key=lambda p: p['rating'])

    # Average price and rating per category
    for product in extracted_products:
        category = product['category']

        if category not in category_statistics:
            category_statistics[category] = {
                'prices_sum': 0,
                'rating_sum': 0,
                'count': 0
            }

        stats = category_statistics[category]

        stats['prices_sum'] += product['price']
        stats['rating_sum'] += product['rating']
        stats['count'] += 1

    for category, stats in category_statistics.items():
        stats['avg_price'] = round(stats['prices_sum'] / stats['count'], 2)
        stats['avg_rating'] = round(stats['rating_sum'] / stats['count'], 2)

        # Unnecessary anymore
        del stats['prices_sum']
        del stats['rating_sum']
        del stats['count']
    
    highest_category = max(category_statistics, key=lambda category: category_statistics[category]['avg_rating'])
    lowest_category = min(category_statistics, key=lambda category: category_statistics[category]['avg_rating'])

    return Results(
        highest_rating=highest_rating,
        lowest_rating=lowest_rating,
        category_statistics=category_statistics,
        highest_category=highest_category,
        lowest_category=lowest_category
    )


def write_summary(path, results):
    summary_path = path / 'summary.txt'

    with summary_path.open('w', newline='', encoding='utf-8') as f:
        f.write('Categories Summary\n')
        f.write('==================\n\n')

        for category, stats in results.category_statistics.items():
            f.write(f'''- {category}:
Average price by category: {stats["avg_price"]:.2f}
Average rating by category: {stats["avg_rating"]:.2f}\n\n''')
            
        f.write('------------------------\n\n')
        f.write('Overall Summary\n')
        f.write('===============\n\n')

        f.write(f'''Highest rated category: {results.highest_category} (average product rating: {results.category_statistics[results.highest_category]["avg_rating"]:.2f})
Lowest rated category: {results.lowest_category} (average product rating: {results.category_statistics[results.lowest_category]["avg_rating"]:.2f})
            
Highest-rated product: {results.highest_rating["title"]} (rating: {results.highest_rating["rating"]})
Lowest-rated product: {results.lowest_rating["title"]} (rating: {results.lowest_rating['rating']})''')
    

def main():
    try:
        products = fetch_products()
    except requests.exceptions.ConnectionError:
        print('Couldn\'t connect to the server')
        return
    except requests.exceptions.Timeout:
        print('The request timed out')
        return
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return
    
    extracted_products = extract_fields(products)
    path = validate_path('Enter folder path: ')
    write_csv(path, extracted_products)
    results = calc_statistics(extracted_products)
    write_summary(path, results)

main()