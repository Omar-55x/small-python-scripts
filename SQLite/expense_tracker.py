''' 
A mini expense tracker program. This program allows multiple features like:
- Adding accounts, categories, expenses
- Listing all expenses
- Searching expenses by category
- Deleting expenses
'''

import argparse
from pathlib import Path
import logging
import sqlite3


def main():
    # Configure parser
    parser = argparse.ArgumentParser(
        description='Track your expenses and accounts'
    )
    parser.add_argument('path', type=Path, help='Enter the path to store reports, data, and logs')
    args = parser.parse_args()

    path = args.path.expanduser().resolve()

    if not path.is_dir():
        parser.error(f'{path} is not an existing folder')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        filename=path / 'expense_tracker.log',
        format='%(asctime)s  %(levelname)s:%(message)s'
    )

    logging.info('Program started')

    # Configure DB
    data_file = path / 'expense_tracker.db'
    try:
        conn = sqlite3.connect(data_file)
        conn.execute("PRAGMA foreign_keys = ON")

        with conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS accounts(
            account_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            institution TEXT,
            type TEXT NOT NULL
            );""")

            c.execute("""CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            );""")

            c.execute("""CREATE TABLE IF NOT EXISTS expenses(
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,

            amount REAL NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL,

            FOREIGN KEY (account_id) REFERENCES accounts(account_id),
            FOREIGN KEY (category_id) REFERENCES caregories(category_id)
            );""")
    except sqlite3.OperationalError:
        logging.exception('Operational Error')
        print('An operational error occured. Check logs for more information.')
        return

    logging.info('Connected to the database')

    print()
    while True:
        print('''What operation do you want to perform?
        1- View all expenses
        2- Search an expense by category
        3- Add an account
        4- Add a category
        5- Add an expense
        6- Delete an expense''')

        command = input('Enter operation number (q to exit): ')
        print()

        match command:
            case 'q' | 'Q':
                logging.info('Program terminated')
                conn.close()
                exit()
            case _:
                print('Invalid input\n')

main()