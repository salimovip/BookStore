import pyodbc

variants = [
    r"LAPTOP-5B8TNS55\SALIMOV",
    r"localhost\SALIMOV",
    r".\SALIMOV",
    r"(local)\SALIMOV",
]

for server in variants:
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;",
            timeout=10
        )
        print("OK:", server)
        conn.close()
        break
    except pyodbc.Error as e:
        print("XATO:", server, "->", str(e)[:150])