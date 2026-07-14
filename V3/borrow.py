"""
borrow.py
Borrowing / returning / due-date management for the Library Management System V3.

Adds a transactions.csv on top of the existing database.csv (books) and
members.csv (members) from V2, without changing their structure.

transactions.csv columns:
transaction_id, book_id, member_id, borrow_date, due_date, return_date, status
    status: "borrowed" or "returned"
"""

import csv
import os
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "transactions.csv")
BOOKS_FILE = os.path.join(BASE_DIR, "database.csv")
MEMBERS_FILE = os.path.join(BASE_DIR, "members.csv")

TRANSACTION_FIELDNAMES = [
    "transaction_id", "book_id", "member_id",
    "borrow_date", "due_date", "return_date", "status"
]

BORROW_PERIOD_DAYS = 14  # how many days a book can be borrowed for


# ---------- Transaction file helpers ----------

def init_transactions_file():
    """Create transactions.csv with headers if it doesn't already exist."""
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDNAMES)
            writer.writeheader()


def get_all_transactions():
    """Return all transactions as a list of dictionaries."""
    init_transactions_file()
    with open(TRANSACTIONS_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_all_transactions(transactions):
    """Overwrite transactions.csv with the given list of transaction dicts."""
    with open(TRANSACTIONS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDNAMES)
        writer.writeheader()
        writer.writerows(transactions)


def generate_transaction_id(transactions):
    """Generate the next transaction ID, e.g. T001, T002, ..."""
    if not transactions:
        return "T001"
    last_num = max(int(t["transaction_id"][1:]) for t in transactions)
    return f"T{last_num + 1:03d}"


# ---------- Book helpers (reads/writes database.csv from books.py) ----------

def get_all_books():
    """Return all books as a list of dictionaries."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        # Guard against stray whitespace in header names (e.g. "book_id " with a trailing space)
        return [{k.strip(): v for k, v in row.items()} for row in reader]


def get_book_by_id(book_id):
    """Return a single book dict by ID, or None if not found."""
    book_id = book_id.strip()
    for book in get_all_books():
        if book.get("book_id", "").strip() == book_id:
            return book
    return None


def update_book_status(book_id, new_status):
    """Update a book's status field (available/taken) in database.csv."""
    books = get_all_books()
    if not books:
        return False

    fieldnames = list(books[0].keys())
    updated = False
    for book in books:
        if book.get("book_id", "").strip() == book_id.strip():
            book["status"] = new_status
            updated = True

    if updated:
        with open(BOOKS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

    return updated


# ---------- Member helper (reads members.csv from members.py) ----------

def member_exists(member_id):
    """Check whether a member ID exists in members.csv."""
    if not os.path.exists(MEMBERS_FILE):
        return False
    with open(MEMBERS_FILE, "r", newline="") as f:
        members = list(csv.DictReader(f))
    return any(m.get("member_id") == member_id for m in members)


# ---------- Core features ----------

def borrow_book():
    """Borrow a book: validates book/member, creates a transaction, updates book status."""
    book_id = input("Enter book ID to borrow: ").strip()
    member_id = input("Enter member ID: ").strip()

    book = get_book_by_id(book_id)
    if book is None:
        print("Book ID not found.")
        return

    if book.get("status", "").lower() != "available":
        print(f"Book '{book.get('title')}' is currently not available (status: {book.get('status')}).")
        return

    if not member_exists(member_id):
        print("Member ID not found.")
        return

    transactions = get_all_transactions()
    transaction_id = generate_transaction_id(transactions)
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=BORROW_PERIOD_DAYS)

    new_transaction = {
        "transaction_id": transaction_id,
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": borrow_date.isoformat(),
        "due_date": due_date.isoformat(),
        "return_date": "",
        "status": "borrowed",
    }

    with open(TRANSACTIONS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDNAMES)
        writer.writerow(new_transaction)

    update_book_status(book_id, "taken")

    print(f"Book borrowed successfully! Transaction ID: {transaction_id}")
    print(f"Due date: {due_date.isoformat()}")


def return_book():
    """Return a book: finds the active transaction for that book and closes it."""
    book_id = input("Enter book ID to return: ").strip()

    transactions = get_all_transactions()
    active_transaction = None
    for t in transactions:
        if t["book_id"] == book_id and t["status"] == "borrowed":
            active_transaction = t
            break

    if active_transaction is None:
        print("No active borrow record found for this book ID.")
        return

    return_date = date.today()
    due_date = date.fromisoformat(active_transaction["due_date"])

    active_transaction["return_date"] = return_date.isoformat()
    active_transaction["status"] = "returned"

    save_all_transactions(transactions)
    update_book_status(book_id, "available")

    print("Book returned successfully.")
    if return_date > due_date:
        days_late = (return_date - due_date).days
        print(f"Note: this book was returned {days_late} day(s) late (due {due_date.isoformat()}).")
    else:
        print("Returned on time.")


def view_due_books():
    """List all currently borrowed books with due dates, flagging overdue ones."""
    transactions = get_all_transactions()
    borrowed = [t for t in transactions if t["status"] == "borrowed"]

    if not borrowed:
        print("No books are currently borrowed.")
        return

    today = date.today()

    print(f"{'Txn ID':<8}{'Book ID':<10}{'Member ID':<12}{'Due Date':<12}{'Status':<12}")
    print("-" * 60)
    for t in borrowed:
        due_date = date.fromisoformat(t["due_date"])
        label = "OVERDUE" if today > due_date else "On time"
        print(f"{t['transaction_id']:<8}{t['book_id']:<10}{t['member_id']:<12}{t['due_date']:<12}{label:<12}")
