# Budget-Padmanabhan

A command-line budget tracker that stores financial data in a local SQLite database.

## Features
- Add income and expense transactions with category, amount, and notes
- View all transactions in a formatted table
- View a summary showing total income, total expenses, and current balance
- Delete transactions by ID

## Requirements
- Python 3.x (no external packages needed — uses the built-in `sqlite3` library)

## How to Run

```bash
python budget.py
```

Follow the on-screen menu to manage your budget:

```
=== Budget Padmanabhan ===
1. Add Income
2. Add Expense
3. View All Transactions
4. Summary
5. Delete Transaction
6. Exit
```

## Data Storage
All transactions are stored in a `budget.db` SQLite database file created automatically in the same directory when you first run the program.
