"""
- Given a directory, this program will seach all '.txt' files for a word entered by the user
- The output includes the file name, number of matches, and line numbers where the match happened
"""

from pathlib import Path
import re


def validate_path(prompt):
    while True:
        path = Path(input(prompt)).expanduser().resolve()

        if not path.exists():
            print(f'"{path}" does not exist')
            continue
        if not path.is_dir():
            print(f'"{path}" is not a directory')
            continue

        return path

# Get text files list
def get_files(path):
    return [p for p in path.iterdir() if p.suffix == '.txt']

# Find matches
def find_matches(files, keyword):
    search_results = []    # list of tuples containing: file_name, match_count, line_nums
    pattern = rf'\b{re.escape(keyword)}\b'

    for file in files:
        match_count = 0
        line_nums = []

        with file.open('r') as f:
            for index, line in enumerate(f, start=1):
                matches = re.findall(pattern, line, flags=re.IGNORECASE)
                if matches:
                    match_count += len(matches)
                    line_nums.append(index)

        search_results.append((file.name, match_count, line_nums))
    
    return search_results

def print_results(search_results):
    for result in search_results:
        file_name, match_count, line_nums = result
        
        match match_count:
            case 0:
                print(f'{file_name} --> No matches')
            case 1:
                print(f'{file_name} --> 1 match at line number {line_nums[0]}')
            case _:
                print(f'{file_name} --> {match_count} matches at lines: {', '.join(str(num) for num in line_nums)}')

def main():
    path = validate_path('Enter directory Path: ')
    files = get_files(path)

    if not files:
        print('The directory does not have text files')
        return

    keyword = input('What word are you looking for?\nKeyword: ')
    print()
    results = find_matches(files, keyword)
    print_results(results)


if __name__ == '__main__':
    main()