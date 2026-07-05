import csv
import os

FILE = "database.csv"


def initialize_database():
    """Create the database file if it doesn't exist."""
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["book_id", "title", "author", "genre", "year", "status"])


def add_book():
    initialize_database()

    book_id = input("Book ID: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    genre = input("Genre: ").strip()
    year = input("Publication Year: ").strip()

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["book_id"] == book_id:
                print("\n❌ Book ID already exists!")
                return

    with open(FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([book_id, title, author, genre, year, "Available"])

    print("\n✅ Book added successfully!")


def view_books():
    initialize_database()

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        books = list(reader)

    if not books:
        print("\nNo books available.")
        return

    print("\n" + "=" * 90)
    print(f"{'Book ID':<10}{'Title':<25}{'Author':<20}{'Genre':<15}{'Year':<8}{'Status'}")
    print("=" * 90)

    for book in books:
        print(
            f"{book['book_id']:<10}"
            f"{book['title']:<25}"
            f"{book['author']:<20}"
            f"{book['genre']:<15}"
            f"{book['year']:<8}"
            f"{book['status']}"
        )

    print("=" * 90)


def search_book():
    initialize_database()

    keyword = input("\nEnter Book ID, Title or Author: ").strip().lower()
    found = False

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print("\n" + "=" * 90)
        print(f"{'Book ID':<10}{'Title':<25}{'Author':<20}{'Genre':<15}{'Year':<8}{'Status'}")
        print("=" * 90)

        for book in reader:
            if (
                keyword == book["book_id"].lower()
                or keyword in book["title"].lower()
                or keyword in book["author"].lower()
            ):
                found = True

                print(
                    f"{book['book_id']:<10}"
                    f"{book['title']:<25}"
                    f"{book['author']:<20}"
                    f"{book['genre']:<15}"
                    f"{book['year']:<8}"
                    f"{book['status']}"
                )

        print("=" * 90)

    if not found:
        print("❌ No matching book found.")


def update_book():
    initialize_database()

    book_id = input("\nEnter Book ID to update: ").strip()

    books = []
    found = False

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for book in reader:

            if book["book_id"] == book_id:
                found = True

                print("\nLeave blank to keep existing value.\n")

                title = input(f"Title [{book['title']}]: ").strip()
                author = input(f"Author [{book['author']}]: ").strip()
                genre = input(f"Genre [{book['genre']}]: ").strip()
                year = input(f"Year [{book['year']}]: ").strip()
                status = input(f"Status [{book['status']}]: ").strip()

                if title:
                    book["title"] = title
                if author:
                    book["author"] = author
                if genre:
                    book["genre"] = genre
                if year:
                    book["year"] = year
                if status:
                    book["status"] = status

            books.append(book)

    if not found:
        print("\n❌ Book not found.")
        return

    with open(FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["book_id", "title", "author", "genre", "year", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)

    print("\n✅ Book updated successfully!")


def delete_book():
    initialize_database()

    book_id = input("\nEnter Book ID to delete: ").strip()

    books = []
    found = False

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for book in reader:
            if book["book_id"] == book_id:
                found = True
                continue

            books.append(book)

    if not found:
        print("\n❌ Book not found.")
        return

    with open(FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["book_id", "title", "author", "genre", "year", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)

    print("\n✅ Book deleted successfully!")
