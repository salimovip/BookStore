import pyodbc
from tabulate import tabulate

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=LAPTOP-5B8TNS55\SALIMOV;"
    "DATABASE=BookStore;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;",
    timeout=60
)
cursor = connection.cursor()
a = cursor.execute(''' use BookStore ''')


class Book:
    @staticmethod
    def get_books():
        query = '''select id,title,author,genre,stock_qty,price from books where stock_qty > 0 '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    @staticmethod
    def get_top_book():
        query = ''' select * from dbo.view_top_books '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        connection.commit()

    @staticmethod
    def add_book():
        book_title = input('Enter Book Name: ').strip()
        book_author = input('Enter Book Author: ').strip()
        book_genre = input('Enter Book Genre: ').strip()
        stock_qty = int(input('Enter Book Quantity: '))
        book_price = float(input('Enter Book Price: '))
        if book_title and book_author and book_genre and stock_qty and book_price:
            query = ''' exec dbo.insert_book ? , ? , ? , ? , ? '''
            result = cursor.execute(query, (book_title, book_author, book_genre, stock_qty, book_price))
            print(' Added successfully ✅')
        else:
            print(' 🚫 Fill all inputs ❗')
        connection.commit()

    @staticmethod
    def update_books_qty():
        admin_password = 'admin123'
        admin_pass = input('Enter admin password: ')

        if admin_pass == admin_password:
            pr_id = int(input('Which product would you like to reserve? '))

            query = '''SELECT * FROM books WHERE id = ?'''
            result = cursor.execute(query, (pr_id,))
            book = result.fetchone()

            if book:
                pr_qty = int(input('How many ?: '))
                current_qty = book[4]  # assuming stock_qty is at index 4
                new_qty = current_qty + pr_qty

                update_query = '''UPDATE books SET stock_qty = ? WHERE id = ?'''
                cursor.execute(update_query, (new_qty, pr_id))
                connection.commit()
                print('Added Successfully ✅')
            else:
                print('Bunday product topilmadi!')
        else:
            print('Wrong credentials 🚫')

    @staticmethod
    def leave_feedback(user_id):
        book_id = int(input(' Enter book ID: '))
        comment = input(' Enter comment: ')
        rating = int(input(' Enter rating for book (1-5): '))
        if book_id and comment and rating:
            query = ''' insert into reviews (user_id,book_id,rating,comment) values (?, ?, ?, ?) '''
            result = cursor.execute(query, (user_id, book_id, rating, comment))
            connection.commit()
            print(' Added successfully!')
        else:
            print(' 🚫 Fill all inputs ❗')
