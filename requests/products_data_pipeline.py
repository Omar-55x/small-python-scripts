'''
- A data pipeline that uses this workflow: API --> JSON --> Extract needed fields --> Save to CSV --> Write text summary (Including logs)

- In this case,
 the API will include information about different proudcts.
 The fields to extract are title, price, category, and rating.
 The summary will include:
   1- The average price and rating for each category.
   2- The products with the highest and lowest rating.
   3- The categories with the highest and lowest average rating.

- API used: https://dummyjson.com/products

- To use the program in the terminal run: py (python3 for macOS/Linux) products_data_pipeline.py "{path}"
'''

import requests
from pathlib import Path
import csv
from dataclasses import dataclass
import argparse
import logging


FIELD_NAMES = ('title', 'category', 'price', 'rating')
API_URL = 'https://dummyjson.com/products'

@dataclass
class Results:
    category_statistics: dict
    highest_category: str
    lowest_category: str
    highest_rating: dict
    lowest_rating: dict


def fetch_products() -> list[dict]:
    logging.info('Fetching products from API')

    products_response = requests.get(API_URL, timeout=10)
    products_response.raise_for_status()
    products = products_response.json()['products']

    logging.info('Retrieved %d products', len(products))

    return products


def extract_fields(products: list[dict]) -> list[dict]:
    extracted_products = []

    for product in products:
        extracted_product = {field: product[field] for field in FIELD_NAMES}
        extracted_products.append(extracted_product)

    logging.info('Extracted %d products', len(extracted_products))

    return extracted_products


# Save products into a CSV file
def write_csv(path: Path, extracted_products: list[dict]) -> None:
    csv_path = path / 'products.csv'


    with csv_path.open('w', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()

        for product in extracted_products:
            csv_writer.writerow(product)

    logging.info('Wrote CSV to %s', csv_path)


def calc_statistics(extracted_products: list[dict]) -> Results:
    category_statistics = {}

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

    logging.info('Calculating statistics for %d categories', len(category_statistics))

    for category, stats in category_statistics.items():
        stats['avg_price'] = round(stats['prices_sum'] / stats['count'], 2)
        stats['avg_rating'] = round(stats['rating_sum'] / stats['count'], 2)

        # Unnecessary anymore
        del stats['prices_sum']
        del stats['rating_sum']
        del stats['count']
    
    highest_category = max(category_statistics, key=lambda category: category_statistics[category]['avg_rating'])
    lowest_category = min(category_statistics, key=lambda category: category_statistics[category]['avg_rating'])

    highest_rating = max(extracted_products, key=lambda p: p['rating'])
    lowest_rating = min(extracted_products, key=lambda p: p['rating'])

    return Results(
        category_statistics=category_statistics,
        highest_category=highest_category,
        lowest_category=lowest_category,
        highest_rating=highest_rating,
        lowest_rating=lowest_rating
    )


def write_summary(path: Path, results: Results) -> None:
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

    logging.info('Wrote summary to %s', summary_path)
    

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Fetch products data, generate CSV, and write text summary'
    )

    parser.add_argument('path', type=Path, help='The folder path to save files in')
    args = parser.parse_args()

    path = args.path.expanduser().resolve()

    if not path.is_dir():
        parser.error(f'{path} is not an existing directory')

    log_path = path / 'products.log'

    logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    format='%(asctime)s  %(levelname)s:%(message)s'
    )

    logging.info('Program started')

    try:
        products = fetch_products()
    except requests.exceptions.ConnectionError:
        logging.error('Couldn\'t connect to the server')
        print('Couldn\'t connect to the server.')
        return
    except requests.exceptions.Timeout:
        logging.error('The request timed out')
        print('The request timed out.')
        return
    except requests.exceptions.RequestException:
        logging.exception('Request failed')
        print('Request failed. See the log file for details.')
        return
    
    extracted_products = extract_fields(products)
    write_csv(path, extracted_products)
    results = calc_statistics(extracted_products)
    write_summary(path, results)

    logging.info('Program completed successfully')


if __name__ == '__main__':
    main()