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


class Inventory:
    @staticmethod
    def backup_logs():
        query = ''' select s1.id,s2.title,change_qty,reason,changed_at from inventory_logs s1
join books s2
on s1.book_id = s2.id '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        connection.commit()

    @staticmethod
    def low_stock_books():
        query = ''' select id,title,author,genre,stock_qty,price from books
where stock_qty < 10 '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print('Kam zaxiradagi kitoblar topilmadi')
        else:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            connection.commit()
