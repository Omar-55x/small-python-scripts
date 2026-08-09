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
from datetime import datetime

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

def get_valid_number(var):
    while True:
        num = input(f'{var}: ').strip()

        if not num:
            print(f'{var} can not be empty')
            continue
        if not num.isnumeric():
            print(f'{var} can only contain numbers')
            continue

        return num


def show_expenses(conn):
    with conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""SELECT
        e.expense_id,
        a.name AS account,
        e.title,
        c.name AS category,
        e.amount,
        e.description
        FROM expenses AS e
        JOIN accounts AS a
            ON e.account_id = a.account_id
        JOIN categories AS c
            ON e.category_id = c.category_id;""")

        records = c.fetchall()

        for record in records:
            print(f'''Expense ID: {record['expense_id']}
Account: {record['account']}
Title: {record['title']}
Category: {record['category']}
Amount: {record['amount']}$
Description: {record['description']}\n\n''')
        
        logging.info('Displayed all expenses;')


def make_account(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT account_id FROM accounts;")
        accounts_ids = {row[0] for row in c.fetchall()}

    new_account = {}

    while True:
            new_account['account_id'] = int(''.join(secrets.choice('0123456789') for _ in range(8)))
    
            if len(str(new_account['account_id'])) != 8:
                continue
    
            if new_account['account_id'] not in accounts_ids:
                break

    new_account['name'] = get_valid_text('Name')
    new_account['institution'] = input('Institution (leave empty if cash): ').strip()
    new_account['type'] = get_valid_text('Type')

    return new_account

    

def add_account(conn, new_account):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO accounts
        (account_id, name, institution, type)
        VALUES
        (?, ?, ?, ?);""",
        (new_account['account_id'], new_account['name'], new_account['institution'], new_account['type']))

        logging.info('New account: %s (%s) has been added to the database', new_account['name'], new_account['account_id'])
        print(f'\n{new_account['name']} has been added to the database\n')


def add_category(conn):
    with conn:
        c = conn.cursor()
        c.execute('SELECT name FROM categories;')
        categories = {row[0] for row in c.fetchall()}

        while True:
            new_category = get_valid_text("New category name (q to exit)")
            print()

            if new_category in categories:
                print('Category already exists')
                continue
            if new_category in ['q', 'Q']:
                return
            
            c.execute("INSERT INTO categories (name) VALUES (?);", (new_category,))

            logging.info('New category: %s has been created', new_category)
            print(f'{new_category} category has been added to the database\n')

            return


def make_expense(conn):
    expense = {}

    with conn:
        c = conn.cursor()

        # Get account name - id
        acc_name = get_valid_text('Account name associated with the expense')

        c.execute("SELECT account_id FROM accounts WHERE name=?;", (acc_name,))
        try:
            expense['acc_id'] = c.fetchone()[0]
        except TypeError:
            print(f'No account found with the name "{acc_name}"')
            logging.warning('No such account name: %s', acc_name)
            raise TypeError

        # Get category name - id
        category_name = get_valid_text('Category')

        c.execute("SELECT category_id FROM categories WHERE name=?;", (category_name,))
        try:
            expense['category_id'] = c.fetchone()[0]
        except TypeError:
            print(f'No category found with the name "{category_name}"\nPlease make the category first or choose an existing category')
            logging.warning('No such category: %s', category_name)
            raise TypeError

        expense['title'] = get_valid_text('Title')
        expense['amount'] = get_valid_number('Amount')
        expense['description'] = input('Description (enter for no description): ').strip()
        expense['expense_date'] = datetime.now().isoformat()

    return expense


def add_expense(conn, expense):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO expenses
        (account_id, category_id, title, amount, description, expense_date)
        VALUES
        (?,?,?,?,?,?);""",
        (expense['acc_id'], expense['category_id'], expense['title'], expense['amount'], expense['description'], expense['expense_date']))

        logging.info('New expense: %s has been added', expense['title'])
        print(f'\n{expense['title']} has been added to the expenses\n')


def search_category(conn):
    with conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT name FROM categories;")
        categories = {row[0] for row in c.fetchall()}

        category = get_valid_text('Category')

        if category not in categories:
            logging.warning('Category: %s not found', category)
            print(f'No category found with the name "{category}"')
            return

        c.execute("SELECT category_id FROM categories WHERE name = ?", (category,))
        category_id = c.fetchone()[0]

        c.execute("""SELECT
        e.expense_id,
        a.name AS account,
        e.title,
        e.amount,
        e.description
        FROM expenses AS e
        JOIN accounts as a
            ON e.account_id = a.account_id
        WHERE e.category_id = ?
        ORDER BY e.amount;""", (category_id,))

        records = c.fetchall()

        print(f'\nRecords in {category} category:\n')

        for record in records:
            print(f'''Expense ID: {record['expense_id']}
Account: {record['account']}
Title: {record['title']}
Amount: {record['amount']}$
Description: {record['description']}\n\n''')


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

            title TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL,

            FOREIGN KEY (account_id) REFERENCES accounts(account_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
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
2- Search expenses by category
3- Add an account
4- Add a category
5- Add an expense
6- Delete an expense''')

        command = input('\nEnter operation number (q to exit): ')
        print()

        match command:
            case '1':
                show_expenses(conn)
            case '2':
                search_category(conn)
            case '3':
                new_account = make_account(conn)
                add_account(conn, new_account)
            case '4':
                add_category(conn)
            case '5':
                try:
                    expense = make_expense(conn)
                except TypeError:
                    return
                
                add_expense(conn, expense)
            case 'q' | 'Q':
                logging.info('Program terminated')
                conn.close()
                exit()
            case _:
                print('Invalid input\n')

main()