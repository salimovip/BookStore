# ---  Global Imports ---
import pyodbc
import re
from tabulate import tabulate
import curses
import pandas

# --- Local Imports ---
import Menus
import Users
import Auth
import Book
import Inventory
import Buy
import Reports 

connection = pyodbc.connect(
    r"DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=LAPTOP-5B8TNS55\SALIMOV;"
    r"DATABASE=BookStore;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;",
    timeout=60
)
cursor = connection.cursor()
a = cursor.execute(''' use BookStore ''')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

command_txt = ''' Enter Command Number: '''
while True:
    Menus.clean_terminal()
    Menus.store_menu()
    command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
    if command_number == 1:
        while True:
            Menus.auth_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                if not Auth.Auth.user:  # not user = kirmagan
                    Auth.Auth.register()
                else:
                    Auth.Auth.acc_details()
            elif command_number == 2:
                if not Auth.Auth.user:
                    Auth.Auth.login()
                else:
                    Auth.Auth.logout()
            elif command_number == 3:
                break
    elif command_number == 2:
        while True:
            Menus.user_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Users.Users.get_all_users()
            elif command_number == 2:
                Users.Users.get_user()
            elif command_number == 3:
                break
    elif command_number == 3:
        while True:
            Menus.book_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                if Auth.Auth.user:
                    Book.Book.add_book()
                else:
                    Book.Book.get_books()
            elif command_number == 2:
                if Auth.Auth.user:
                    Book.Book.update_books_qty()
                else:
                    Book.Book.get_top_book()
            elif command_number == 3:
                if Auth.Auth.user:
                    Book.Book.get_books()
                else:
                    break
            elif command_number == 4:
                if Auth.Auth.user:
                    Book.Book.get_top_book()
            elif command_number == 5:
                if Auth.Auth.user:
                    query = "SELECT id FROM users WHERE email = ?"
                    user_id = cursor.execute(query, (Auth.Auth.info['user_email'],))
                    result = user_id.fetchall()
                    Book.Book.leave_feedback(result[0][0])
                else:
                    pass
            elif command_number == 6:
                if Auth.Auth.user:
                    break
    elif command_number == 4:
        while True:
            Menus.orders_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if not Auth.Auth.user:
                print(f' {Bcolors.WARNING} You Should ( Register / login) to buy a new book(s) {Bcolors.ENDC}')
            if Auth.Auth.user:
                if command_number == 1:
                    query = "SELECT id FROM users WHERE email = ?"
                    user_id = cursor.execute(query, (Auth.Auth.info['user_email'],))
                    result = user_id.fetchall()
                    Buy.BuyBook.create_order(result[0][0])
            else:
                break

            if Auth.Auth.user:
                if command_number == 2:
                    Buy.BuyBook.decline_order()
            if Auth.Auth.user:
                if command_number == 3:
                    Buy.BuyBook.see_orders()
            if Auth.Auth.user:
                if command_number == 4:
                    break
    elif command_number == 5:
        while True:
            Menus.inventory_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Inventory.Inventory.backup_logs()
            elif command_number == 2:
                Inventory.Inventory.low_stock_books()
            elif command_number == 3:
                break
    elif command_number == 6:
        while True:
            Menus.reports_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Reports.Reports.monthly_reports()
            elif command_number == 2:
                Reports.Reports.top_buyers()
            elif command_number == 3:
                Reports.Reports.top_reviewed_books()
            elif command_number == 4:
                break
    elif command_number == 7:
        break
cursor.close()
connection.close()