# Library Management System

A simple, menu-driven Library Management System built in Python, using CSV files for data storage. This repo tracks the evolution of the project across versions.

## Versions

### V1 — Book Management
- Add Book
- View Books
- Search Book
- Update Book
- Delete Book

Data is stored in `database.csv` with the columns:
`bookid, title, author, genre, year, status (available/taken)`

### V2 — Adds Member Management
Builds on V1 by introducing member registration and management, alongside all existing book features.

**New features:**
- Register Member
- View Members
- Search Member
- Delete Member

Member data is stored separately in `members.csv` with the columns:
`member_id, name, email, phone, join_date`

Member IDs are auto-generated in the format `M001`, `M002`, etc.

## Project Structure

```
Library-Management-System/
├── V1/
│   ├── main.py        # Menu system (books only)
│   ├── books.py        # Book management functions
│   └── database.csv    # Book records
│
├── V2/
│   ├── main.py          # Menu system (books + members)
│   ├── books.py         # Book management functions
│   ├── members.py       # Member management functions
│   ├── database.csv     # Book records
│   └── members.csv      # Member records
```

## How to Run

Navigate into the version folder you want to run and start `main.py`:

```bash
cd V2
python main.py
```

## Menu (V2)

```
========================================
 LIBRARY MANAGEMENT SYSTEM
========================================
1. Add Book
2. View Book
3. Search Book
4. Update Book
5. Delete Book
6. Register Member
7. View Member
8. Search Member
9. Delete Member
0. Exit
```

## Tech Stack
- Python 3
- CSV file storage (no external database required)

## Author
Abel Robin
