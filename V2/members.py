"""
members.py
Member management functions for the Library Management System V2.
Stores member data in members.csv with columns:
member_id, name, email, phone, join_date
"""

import csv
import os
from datetime import date

# Always resolve members.csv relative to this file's own location,
# so it doesn't matter which folder the program is launched from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMBERS_FILE = os.path.join(BASE_DIR, "members.csv")
FIELDNAMES = ["member_id", "name", "email", "phone", "join_date"]


def init_members_file():
    """Create members.csv with headers if it doesn't already exist."""
    if not os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def get_all_members():
    """Return all members as a list of dictionaries."""
    init_members_file()
    with open(MEMBERS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def generate_member_id(members):
    """Generate the next member ID, e.g. M001, M002, ..."""
    if not members:
        return "M001"
    last_num = max(int(m["member_id"][1:]) for m in members)
    return f"M{last_num + 1:03d}"


def register_member():
    """Register a new member and save to members.csv."""
    members = get_all_members()

    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()
    phone = input("Enter member phone: ").strip()
    join_date = date.today().isoformat()
    member_id = generate_member_id(members)

    new_member = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone,
        "join_date": join_date,
    }

    with open(MEMBERS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(new_member)

    print(f"Member registered successfully! ID: {member_id}")


def print_members_table(members):
    """Print members in a table with column widths based on the longest value in each column."""
    headers = {"member_id": "ID", "name": "Name", "email": "Email", "phone": "Phone", "join_date": "Join Date"}

    # Start each column width at the header's length, then grow it to fit the widest value
    widths = {key: len(label) for key, label in headers.items()}
    for m in members:
        for key in headers:
            widths[key] = max(widths[key], len(m.get(key, "")))

    # Add a little padding so columns aren't crammed together
    for key in widths:
        widths[key] += 2

    header_row = "".join(headers[key].ljust(widths[key]) for key in headers)
    print(header_row)
    print("-" * len(header_row))

    for m in members:
        row = "".join(m.get(key, "").ljust(widths[key]) for key in headers)
        print(row)


def view_members():
    """Display all registered members in a table."""
    members = get_all_members()
    if not members:
        print("No members found.")
        return

    print_members_table(members)


def search_member():
    """Search members by ID or name (partial, case-insensitive)."""
    keyword = input("Enter member ID or name to search: ").strip().lower()
    members = get_all_members()
    results = [
        m for m in members
        if keyword in m["member_id"].lower() or keyword in m["name"].lower()
    ]

    if not results:
        print("No matching members found.")
        return

    print_members_table(results)


def delete_member():
    """Delete a member by ID."""
    member_id = input("Enter member ID to delete: ").strip()
    members = get_all_members()
    updated = [m for m in members if m["member_id"] != member_id]

    if len(updated) == len(members):
        print("Member ID not found.")
        return

    with open(MEMBERS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated)

    print("Member deleted successfully.")
