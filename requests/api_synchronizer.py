'''
- Given an api that returns many objects (users in this case) each one associated with an ID, this program will:
1) Download and save the data as JSON
2) On the next run, compare the new data with the saved data
3) Report: new records, deleted records, and modified records
'''

import requests
from pathlib import Path
from datetime import datetime
import json
from dataclasses import dataclass


@dataclass
class Results:
    added: list[str]
    deleted: list[str]
    modified: list[str]


API_URL = 'https://retoolapi.dev/lQowuf/data'


# Get snapshots path
def validate_path(prompt:str) -> tuple[Path, Path]:

    while True:
        path = Path(input(prompt)).resolve().expanduser()
        report_path = path.joinpath('sync_snapshot.txt')
        json_path = path.joinpath('snapshot.json')

        if not path.exists():
            print(f'{path} does not exist')
            continue
        if not path.is_dir():
            print(f'{path} is not a directory')
            continue

        return report_path, json_path


# Fetch API data
def fetch_data() -> list[dict]:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        return r.json()


# If does not exists: save records and generate a new report
def gen_report(report_path: Path, json_path: Path, new_data: list[dict]) -> None:

    # JSON to be used as old data for comparison
    with json_path.open('w', newline='', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4)

    # Actual user friendly formatted text file
    with report_path.open('w', newline='', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'Snapshot {timestamp}\n')
        f.write('----------------------------\n\n')

        for record in new_data:
            for key, value in record.items():
                f.write(f'{key}: {value}\n')
            f.write('\n')
        
        f.write(f"\n- Added {len(new_data)} records:\n\t{'\n\t'.join(record['name'] for record in new_data)}\n\n")
        f.write('============================\n\n')
    
    print(f'Snapshot saved at {report_path}')


# Else: Compare new_data to the old snapshot.json
def compare_snapshots(json_path: Path, new_data: list[dict]) -> Results:

    with json_path.open('r', encoding='utf-8') as json_file:
        old_data = json.load(json_file)

    old_records = {record['id']: record for record in old_data}
    new_records = {record['id']: record for record in new_data}

    added, deleted, modified = [], [], []

    for rec_id, record in new_records.items():
        # If ID is only in the new records
        if rec_id not in old_records:
            added.append(record['name'])
        else:
            # If IDs exist in both places but content is modified
            if record != old_records[rec_id]:
                modified.append(record['name'])

    for rec_id, record in old_records.items():
        # If ID is only in the old records
        if rec_id not in new_records:
            deleted.append(record['name'])

    # Overwrite JSON file
    with json_path.open('w', newline='', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, indent=4)

    return Results(
        added=added,
        deleted=deleted,
        modified=modified
    )



# Add the new snapshot
def add_snapshot(report_path: Path, new_data: list[dict], results: Results) -> None:

    with report_path.open('a', newline='', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'Snapshot {timestamp}\n')
        f.write('----------------------------\n\n')

        for record in new_data:
            for key, value in record.items():
                f.write(f'{key}: {value}\n')
            f.write('\n')
        
        if results.added:
            f.write(f"\n- Added {len(results.added)} records:\n\t{'\n\t'.join(results.added)}\n")
        if results.deleted:
            f.write(f"\n- Deleted {len(results.deleted)} records:\n\t{'\n\t'.join(results.deleted)}\n")
        if results.modified:
            f.write(f"\n- Modified {len(results.modified)} records:\n\t{'\n\t'.join(results.modified)}\n")
        f.write('\n============================\n\n')
        
        print(f'Snapshot saved at {report_path}')


def main() -> None:

    report_path, json_path = validate_path('Enter folder path to save the snapshot: ')

    try:
        new_data = fetch_data()
    except requests.exceptions.ConnectionError:
        print('Couldn\'t connect to the server')
        return
    except requests.exceptions.Timeout:
        print('The request timed out')
        return
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return

    if not report_path.exists():
        gen_report(report_path, json_path, new_data)
        return

    try:
        results = compare_snapshots(json_path, new_data)
    except json.JSONDecodeError:
        print('Invalid JSON')
        return
    
    add_snapshot(report_path, new_data, results)

main()