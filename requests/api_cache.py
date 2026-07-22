'''
- A cache to store API responses locally

- For this case, the API will have countries info that will be stored as "cache/countryName.json" in the provided path
- The cache will expire after 10 minutes

- Do not forget to add the path in which the cache folder will be stored
- API used: https://countries.dev/name/{countryName}
'''


from pathlib import Path
import requests
import json
from datetime import datetime, timedelta


API_URL= 'https://countries.dev/name/'
SOURCE_PATH = Path('D:/Python/Scripting/Core/test')
CACHE_FOLDER = SOURCE_PATH / 'cache'
CACHE_DURATION = timedelta(minutes=10)


def validate_name() -> str | None:
    while True:
        country = input('Enter country name (q to exit): ').strip().lower()

        if not country:
            print('Please enter country name')
            continue
        if not all(char.isalpha() or char.isspace() for char in country):
            print('Country name can not include non-alphabetical characters')
            continue
        if country == 'q':
            return None

        return country


def fetch_data(country: str) -> dict:
    country_response = requests.get(API_URL + country, timeout=10)
    country_response.raise_for_status()
    return country_response.json()[0]


# Cache not found or expired
def save_cache(cache_path: Path, country_info: dict) -> None:
    with cache_path.open('w', newline='', encoding='utf-8') as f:
        country_info['cached_at'] = datetime.now().isoformat()
        json.dump(country_info, f, indent=4)


# Cache is valid
def load_cache(cache_path: Path) -> None:
    with cache_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def check_validity(cache_path: Path) -> bool:
    with cache_path.open('r', encoding='utf-8') as f:
        cache = json.load(f)
        cached_time = datetime.fromisoformat(cache['cached_at'])

        # Check if cache is still valid
        return  datetime.now() - cached_time < CACHE_DURATION
        

def main() -> None:
    country = validate_name()

    if country is None:
        return

    if not CACHE_FOLDER.exists():
        CACHE_FOLDER.mkdir(parents=True, exist_ok=True)
    
    cache_path = CACHE_FOLDER / f'{country}.json'

    try:
        if cache_path.exists():
            status = check_validity(cache_path)
            
            if status:
                print('Loaded from cache')
                cache = load_cache(cache_path)
                print(cache)
            else:
                print('Cache expired. Fetching data from API...')
                country_info = fetch_data(country)
                save_cache(cache_path, country_info)
                print(country_info)
        else:
            print('No cache. Fetching data from API...')
            country_info = fetch_data(country)
            save_cache(cache_path, country_info)
            print(country_info)
    except requests.exceptions.Timeout:
        print('Connection timed out')
        return
    except requests.exceptions.ConnectionError:
        print('Couldn\'t connect to the server')
        return
    except requests.exceptions.HTTPError:
        print('Country not found')
        return
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return
    except json.JSONDecodeError:
        print(f'Invalid JSON')
        return
    
main()