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

def get_valid_amount():
    while True:
        amount = input('Amount: ').strip()

        try:
            amount = float(amount)

            if amount <= 0:
                print('Amount must be greater than zero')
                continue

            return amount

        except ValueError:
            print('Please enter a valid number')


def show_expenses(conn):
    with conn:
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


def make_account():
    new_account = {}
    new_account['name'] = get_valid_text('Name')
    new_account['institution'] = input('Institution (leave empty if cash): ').strip()
    new_account['type'] = get_valid_text('Type')

    return new_account

    

def add_account(conn, new_account):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO accounts
        (name, institution, type)
        VALUES
        (?, ?, ?);""",
        (new_account['name'], new_account['institution'], new_account['type']))

        logging.info('New account: %s has been added to the database', new_account['name'])
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
        row = c.fetchone()

        if row is None:
            print(f'No account found with the name "{acc_name}"')
            logging.warning('No such account name: %s', acc_name)
            return None
        
        expense['acc_id'] = row[0]

        # Get category name - id
        category_name = get_valid_text('Category')

        c.execute("SELECT category_id FROM categories WHERE name=?;", (category_name,))
        row = c.fetchone()

        if row is None:
            print(f'No category found with the name "{category_name}"\nPlease make the category first or choose an existing category')
            logging.warning('No such category: %s', category_name)
            return None
        
        expense['category_id'] = row[0]

        expense['title'] = get_valid_text('Title')
        expense['amount'] = get_valid_amount()
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

        logging.info('Displayed all expenses in %s category', category)


def delete_expense(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT expense_id FROM expenses;")
        ids = {row[0] for row in c.fetchall()}

        expense_id = input('Expense ID: ')

        try:
            expense_id = int(expense_id)
        except ValueError:
            print('Expense ID must be a number')
            return

        if expense_id not in ids:
            logging.warning('No expense found with the ID %d', expense_id)
            print(f'No expense found with the ID {expense_id}')
            return

        c.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        logging.info('Deleted expense. ID: %d', expense_id)
        print(f'\nExpense {expense_id} was deleted successfully\n')


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
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        with conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS accounts(
            account_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            institution TEXT,
            type TEXT NOT NULL
            );""")

            c.execute("""CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
            );""")

            c.execute("""CREATE TABLE IF NOT EXISTS expenses(
            expense_id INTEGER PRIMARY KEY,
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
                expense = make_expense(conn)

                if expense is not None:
                    add_expense(conn, expense)
            case '6':
                delete_expense(conn)
            case 'q' | 'Q':
                logging.info('Program terminated')
                conn.close()
                exit()
            case _:
                print('Invalid input\n')

main()