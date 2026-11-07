# BookStore Management System

> A command-line book store application for managing a catalogue, customers, orders, inventory, and sales reporting.

**Tech:** Python · Microsoft SQL Server · T-SQL · PyODBC · SQLAlchemy · Pandas

## Highlights

- Browse available books and identify top-selling titles.
- Register customers, view account details, and inspect order history.
- Create multi-item orders with stock validation; cancel pending orders.
- Add books, update stock, view inventory changes, and flag low-stock items.
- Capture book ratings/reviews and export monthly sales and top-rated-book reports as CSV.

## Data & SQL design

The relational database models `users`, `books`, `orders`, `order_items`, `inventory_logs`, and `reviews`.
The SQL layer demonstrates stored procedures, views, a scalar function, joins, constraints, and an `AFTER INSERT` trigger that records inventory movements when order items are created.

## Project structure

```text
main.py             # CLI entry point and menus
sql_code.sql        # Database schema, seed data, procedures, views, trigger
Auth/               # Registration, login, session state
Book/               # Catalogue, stock, and reviews
Buy/                # Cart and order workflow
Inventory/          # Inventory logs and low-stock checks
Reports/            # SQL-backed CSV reporting
Users/              # Customer and order-history queries
```

## Run locally

**Prerequisites:** Python 3.10+, Microsoft SQL Server, and ODBC Driver 18 for SQL Server.

```bash
git clone <your-repository-url>
cd book-project
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

1. Execute `sql_code.sql` in SQL Server Management Studio to create and seed the `BookStore` database.
2. In `main.py` and the module files, replace `LAPTOP-5B8TNS55\SALIMOV` with your SQL Server instance name.
3. Start the application:

```bash
python main.py
```

Generated report files are written to `Report_files/monthly_reports.csv` and `top_rated_books.csv`.

## Resume-ready summary

Built a Python and SQL Server CLI application that implements a normalized book-store data model, transactional order workflow, stock monitoring, and CSV-based business reporting. Used T-SQL procedures, views, and triggers alongside PyODBC, SQLAlchemy, and Pandas.

## Future improvements

- Centralize database configuration with environment variables.
- Add role-based access control, automated tests, and a web interface.
