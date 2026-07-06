"""
Given a file path, this program will return the following information:
1) Number of lines
2) Number of words
3) Number of characters
4) Longest line
5) Shortest line
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Results:
    line_count: int
    word_count: int
    char_count: int
    longest: int
    shortest: int
    

def validate_path(prompt):
    while True:
        path = Path(input(prompt)).expanduser().resolve()

        if not path.exists():
            print(f'"{path}" does not exist')
            continue
        if not path.is_file():
            print(f'"{path}" is not a file')
            continue
        if path.suffix != '.txt':
            print('The file is not a text file')
            continue

        return path

# Function will be required more than once to count chars
def count_chars(content):
    char_count = 0

    for char in content:
        if char not in (' ', '\n'):
            char_count +=1

    return char_count

# Find the requirements
def gather_info(path):
    with path.open('r', encoding='utf-8') as f:
        f_content = f.read()

        # Check if the file is empty
        if not f_content:
            return None

        lines = f_content.splitlines()
        line_count = len(lines)

        word_count = 0
        for line in lines:
            word_count += len(line.split())

        char_count = count_chars(f_content)
        
        longest_count, shortest_count = -1, float('inf')        # Character counters for the lines
        longest, shortest = 0, 0        # Actual line numbers

        for index, line in enumerate(lines):
            count = count_chars(line)

            if longest_count < count:
                longest_count = count
                longest = index + 1
            if shortest_count > count:
                shortest_count = count
                shortest = index + 1

    return Results(
        line_count=line_count,
        word_count=word_count,
        char_count=char_count,
        longest=longest,
        shortest=shortest
    )

def main():
    path = validate_path('Enter file path: ')

    results = gather_info(path)

    if results is None:
        print('File is empty')
    else:
        print(f'Number of lines: {results.line_count}')
        print(f'Number of words: {results.word_count}')
        print(f'Number of characters: {results.char_count}')
        print(f'Longest line number: {results.longest}')
        print(f'Shortest line number: {results.shortest}')


if __name__ == '__main__':
    main()