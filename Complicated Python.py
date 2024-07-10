import json

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            return True
        return False

    def return_book(self):
        self.available = True

    def to_dict(self):
        return {'title': self.title, 'author': self.author, 'available': self.available}

    @classmethod
    def from_dict(cls, data):
        book = cls(data['title'], data['author'])
        book.available = data['available']
        return book


class Library:
    def __init__(self, filename):
        self.filename = filename
        self.books = self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book and book.borrow():
            self.save_books()
            return True
        return False

    def return_book(self, title):
        book = self.find_book(title)
        if book:
            book.return_book()
            self.save_books()
            return True
        return False

    def load_books(self):
        try:
            with open(self.filename, 'r') as f:
                books_data = json.load(f)
                return [Book.from_dict(book) for book in books_data]
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.filename, 'w') as f:
            books_data = [book.to_dict() for book in self.books]
            json.dump(books_data, f, indent=4)


def main():
    library = Library('books.json')

    while True:
        print("\nLibrary Menu:")
        print("1. Add Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            book = Book(title, author)
            library.add_book(book)
            print(f"Book '{title}' by {author} added to the library.")

        elif choice == '2':
            title = input("Enter book title to borrow: ")
            if library.borrow_book(title):
                print(f"You have borrowed '{title}'.")
            else:
                print(f"Sorry, '{title}' is not available or does not exist.")

        elif choice == '3':
            title = input("Enter book title to return: ")
            if library.return_book(title):
                print(f"Thank you for returning '{title}'.")
            else:
                print(f"Sorry, '{title}' does not exist in our records.")

        elif choice == '4':
            print("Exiting the library system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
