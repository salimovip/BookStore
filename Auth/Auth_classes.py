import pyodbc
import re
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


class Auth:
    user = False
    info = {}

    @staticmethod
    def acc_details():
        query = "exec dbo.get_user_info ? , ? "
        result = cursor.execute(query, (Auth.info['user_name'], Auth.info['user_email']))
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        # print(Auth.info)

    @staticmethod
    def register():
        user_name = input(' Ismingizni kiriting: ').strip()
        user_email = input(' Emailingizni kiriting: ').strip()
        query = '''exec dbo.get_user_info ? , ? '''
        result = cursor.execute(query, (user_name, user_email))
        if result.fetchone():
            Auth.info['user_name'] = user_name
            Auth.info['user_email'] = user_email
            Auth.user = True
            print(" ✅ Ro‘yxatdan o‘tish muvaffaqiyatli!")
            # print(Auth.info)
        else:
            print(' ❌ Malumotlar topilmadi !')

    @staticmethod
    def login():
        user_name = input(' Ismingizni kiriting: ').title()
        user_email = input(' Emailingizni kiriting: ')
        user_phone = input(' Enter your phone number: ').replace('+', '').replace(' ', '').replace('-', '')
        check = re.match('\\d{3}\\d{2}\\d{3}\\d{2}\\d{2}', user_phone)
        check_1 = re.match(
            r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",
            user_email)
        query = f''' exec dbo.get_user_info_v2 ? , ? , ? '''
        result_1 = cursor.execute(query, (user_name, user_email, user_phone))
        if not result_1.fetchone():
            if check and check_1:
                Auth.info['user_name'] = user_name
                Auth.info['user_email'] = user_email
                Auth.info['user_phone'] = user_phone
                query = ''' exec dbo.insert_user ? , ? , ? '''
                result = cursor.execute(query, (user_name, user_email, int(user_phone)))
                Auth.user = True
                print(" ✅ Tizimga muvaffaqiyatli kirdimgiz!")
                connection.commit()  # save changes
            else:
                print('Xato malumot kirindingiz!')
        else:
            print('Malumotlar bazada mavjud')

    @staticmethod
    def logout():
        if Auth.user:
            Auth.user = False
            Auth.info.clear()
            print(" 🚪 Siz tizimdan chiqdingiz.")