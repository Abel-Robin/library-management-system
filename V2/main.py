from books import add_book, view_books, search_book, update_book , delete_book
import members
def main():
    while True:
        print("\n==============================")
        print(" LIBRARY MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Add Book")
        print("2. View Book")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Register Member")
        print("7. View Member")
        print("8. Search Member")
        print("9. Delete Member")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()

        elif choice=="2":
            view_books()

        elif choice=="3":
            search_book()

        elif choice=="4":
            update_book()

        elif choice=="5":
            delete_book()
            
        elif choice=="6":
            members.register_member()
            
        elif choice=="7":
            members.view_members()
            
        elif choice=="8":
            members.search_member()
            
        elif choice=="9":
            members.delete_member()

        elif choice=="0":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
