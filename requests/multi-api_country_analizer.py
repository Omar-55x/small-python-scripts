'''
- Given a country name, this program will:
1) Fetch country information from a country API
2) Fetch current exchange rate information from another API
3) Produce a report of the information

- Note: This script will have no config file. For exchange rates request, paste your API key from: https://www.exchangerate-api.com/
''' 

import requests
from pathlib import Path


country = input('Country: ').lower()

try:
    country_response = requests.get(f'https://countries.dev/name/{country}', timeout=10)
    country_response.raise_for_status()
    country_list = country_response.json()

    country_info = country_list[0]

    capital = country_info['capital']
    population = country_info['population']
    region = country_info['region']
    currency = country_info['currencies'][0]['code']

    exchange_response = requests.get('https://v6.exchangerate-api.com/v6/<API_KEY>/latest/USD', timeout=10)
    exchange_response.raise_for_status()
    exc_rates = exchange_response.json()
except requests.exceptions.Timeout:
    print('The request timed out')
    exit()
except requests.exceptions.ConnectionError:
    print('Couldn\'t connect to the server')
    exit()
except requests.exceptions.HTTPError:
    print('Country not found')
    exit()
except requests.exceptions.RequestException as e:
    print(f'Request failed: {e}')
    exit()
except ValueError:
    print('Invalid JSON')
    exit()

while True:
    path = Path(input('Select folder path: '))
    report_path = path.joinpath('Country report.txt')

    if not path.exists():
        print(f'{path} does not exist')
        continue
    if not path.is_dir():
        print(f'{path} is not a directory')
        continue

    break

with report_path.open('a', newline='', encoding='utf-8') as f:
    f.write(f"Country: {country_info['name']}\n")
    f.write(f"\nCapital: {capital}\nPopulation: {population:,}\nRegion: {region}\n\nCurrency: {currency}\n")
    f.write(f"1 USD = {exc_rates['conversion_rates'][f'{currency}']} {currency}\n")
    f.write("\n-----------------------\n\n")

    print('Country info has been added to the report')