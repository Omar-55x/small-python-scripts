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
import secrets

# Helper functions
def get_valid_text(var):
    while True:
        text = input(f'{var}: ').strip()

        if not text:
            print(f'{var} can not be empty')
            continue
        if not all(char.isalpha() or char.isspace() for char in text):
            print(f'{var} can not contain non-alphabetical characters')
            continue

        return text


def show_expenses(conn):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM expenses')
        records = c.fetchall()

        for record in records:
            print(record)

        logging.info('Displayed all expenses')


def make_account(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT account_id FROM accounts")
        accounts_ids = {row[0] for row in c.fetchall()}

    new_account = {}

    while True:
            new_account['account_id'] = int(''.join(secrets.choice('0123456789') for _ in range(8)))
    
            if len(str(new_account['account_id'])) != 8:
                continue
    
            if new_account['account_id'] not in accounts_ids:
                break

    new_account['name'] = get_valid_text('Name')
    new_account['institution'] = get_valid_text('Institution')
    new_account['type'] = get_valid_text('Type')

    return new_account

    

def add_account(conn, new_account):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO accounts
        (account_id, name, institution, type)
        VALUES
        (?, ?, ?, ?)""",
        (new_account['account_id'], new_account['name'], new_account['institution'], new_account['type']))

        logging.info('New account: %s (%s) has been added to the database\n', new_account['name'], new_account['account_id'])
        print(f'\n{new_account['name']} has been added to the database\n')


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

        command = input('\nEnter operation number (q to exit): ')
        print()

        match command:
            case '1':
                show_expenses(conn)
            case '3':
                new_account = make_account(conn)
                add_account(conn, new_account)
            case 'q' | 'Q':
                logging.info('Program terminated')
                conn.close()
                exit()
            case _:
                print('Invalid input\n')

main()