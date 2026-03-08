import sqlite3
import datetime


DB_NAME = "budget.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date      TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            type      TEXT    NOT NULL CHECK(type IN ('income','expense')),
            amount    REAL    NOT NULL,
            note      TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_transaction(category, ttype, amount, note="", date=None):
    if date is None:
        date = datetime.date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (date, category, type, amount, note) VALUES (?, ?, ?, ?, ?)",
        (date, category, ttype, amount, note),
    )
    conn.commit()
    conn.close()
    print(f"  Added {ttype}: {category} ₹{amount:.2f}")


def view_transactions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, date, category, type, amount, note FROM transactions ORDER BY date")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("  No transactions found.")
        return
    print(f"\n  {'ID':<5} {'Date':<12} {'Category':<20} {'Type':<10} {'Amount':>10}  Note")
    print("  " + "-" * 65)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<12} {row[2]:<20} {row[3]:<10} ₹{row[4]:>9.2f}  {row[5]}")


def summary():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='income'")
    total_income = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='expense'")
    total_expense = c.fetchone()[0]
    conn.close()
    balance = total_income - total_expense
    print(f"\n  Total Income :  ₹{total_income:>10.2f}")
    print(f"  Total Expense:  ₹{total_expense:>10.2f}")
    print(f"  Balance      :  ₹{balance:>10.2f}")
    if balance < 0:
        print("  ⚠  Warning: Expenses exceed income!")


def delete_transaction(txn_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    if c.rowcount:
        print(f"  Transaction {txn_id} deleted.")
    else:
        print(f"  Transaction {txn_id} not found.")
    conn.commit()
    conn.close()


def menu():
    init_db()
    while True:
        print("\n=== Budget Padmanabhan ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Summary")
        print("5. Delete Transaction")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            category = input("  Category (e.g. Salary, Freelance): ").strip()
            try:
                amount = float(input("  Amount (₹): ").strip())
            except ValueError:
                print("  Invalid amount. Please enter a number.")
                continue
            note = input("  Note (optional): ").strip()
            add_transaction(category, "income", amount, note)

        elif choice == "2":
            category = input("  Category (e.g. Rent, Food, Transport): ").strip()
            try:
                amount = float(input("  Amount (₹): ").strip())
            except ValueError:
                print("  Invalid amount. Please enter a number.")
                continue
            note = input("  Note (optional): ").strip()
            add_transaction(category, "expense", amount, note)

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            summary()

        elif choice == "5":
            view_transactions()
            try:
                txn_id = int(input("  Enter transaction ID to delete: ").strip())
            except ValueError:
                print("  Invalid ID. Please enter a number.")
                continue
            delete_transaction(txn_id)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("  Invalid option. Please try again.")


if __name__ == "__main__":
    menu()
