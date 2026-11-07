-- ============================================================
-- BookStore Management System
-- Ma'lumotlar bazasi, jadvallar, obyektlar va boshlang'ich ma'lumotlar
-- ============================================================

CREATE DATABASE BookStore;
GO

USE BookStore;
GO

-- ============================================================
-- JADVALLAR
-- ============================================================

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    phone NVARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE books (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    genre NVARCHAR(50) NOT NULL,
    stock_qty INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    added_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10, 2) NOT NULL,
    status NVARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')) NOT NULL,
    ordered_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT,
    book_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE inventory_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    book_id INT,
    change_qty INT NOT NULL,
    reason NVARCHAR(255) NOT NULL,
    changed_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    book_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
GO

-- ============================================================
-- BOSHLANG'ICH MA'LUMOTLAR
-- ============================================================

INSERT INTO users (name, email, phone) VALUES
('Ali Karimov', 'ali.karimov@mail.com', '998901234567'),
('Nodira Xusanova', 'nodira.xusanova@mail.com', '998912345678'),
('Javlon Tursunov', 'javlon.tursunov@mail.com', '998931234589');

INSERT INTO books (title, author, genre, stock_qty, price) VALUES
('Python for Beginners', 'John Doe', 'Programming', 100, 25.99),
('The Data Scientist Handbook', 'Jane Smith', 'Data Science', 50, 45.00),
('The Art of War', 'Sun Tzu', 'Philosophy', 200, 12.99);

INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 25.99, 'completed'),
(2, 91.99, 'pending'),
(3, 55.99, 'cancelled');

INSERT INTO order_items (order_id, book_id, quantity, price) VALUES
(1, 1, 1, 25.99),
(2, 1, 2, 25.99),
(2, 2, 1, 45.00),
(3, 2, 1, 45.00);

INSERT INTO inventory_logs (book_id, change_qty, reason) VALUES
(1, -1, 'Sale'),
(2, -3, 'Sale'),
(3, -5, 'Sale');

INSERT INTO reviews (user_id, book_id, rating, comment) VALUES
(1, 1, 5, 'Excellent book for beginners!'),
(2, 2, 4, 'Very informative, but a bit difficult to follow.'),
(3, 3, 5, 'A timeless classic!');
GO

-- ============================================================
-- FUNKSIYALAR
-- ============================================================

CREATE FUNCTION dbo.InitCap (@input NVARCHAR(MAX))
RETURNS NVARCHAR(MAX)
AS
BEGIN
    DECLARE @result NVARCHAR(MAX) = '',
            @i INT = 1,
            @c CHAR(1),
            @prev CHAR(1) = ' '

    WHILE @i <= LEN(@input)
    BEGIN
        SET @c = SUBSTRING(@input, @i, 1)

        IF @prev = ' '
            SET @result = @result + UPPER(@c)
        ELSE
            SET @result = @result + LOWER(@c)

        SET @prev = @c
        SET @i = @i + 1
    END

    RETURN @result
END;
GO

-- ============================================================
-- PROSEDURALAR: FOYDALANUVCHILAR
-- ============================================================

CREATE PROCEDURE dbo.user_exists
    @user_name varchar(35),
    @user_email varchar(50)
AS
    SELECT * FROM users
    WHERE name = @user_name AND email = @user_email
RETURN 0;
GO

CREATE PROCEDURE dbo.get_user_info
    @user_name varchar(35),
    @user_email varchar(45)
AS
    SELECT id, name, email, phone FROM users
    WHERE name = @user_name AND email = @user_email
RETURN 0;
GO

CREATE PROCEDURE dbo.get_user_info_v2
    @user_name varchar(35),
    @user_email varchar(45),
    @user_phone bigint
AS
    SELECT id, name, email, phone FROM users
    WHERE name = @user_name AND email = @user_email AND phone = @user_phone
RETURN 0;
GO

CREATE PROCEDURE dbo.insert_user
    @user_name varchar(35),
    @user_email varchar(45),
    @user_phone bigint
AS
    INSERT INTO users (name, email, phone) VALUES (@user_name, @user_email, @user_phone)
RETURN 0;
GO

-- ============================================================
-- PROSEDURALAR: KITOBLAR
-- ============================================================

CREATE PROCEDURE dbo.insert_book
    @book_title varchar(45),
    @book_author varchar(35),
    @genre varchar(30),
    @stock_qty int,
    @price float
AS
    INSERT INTO books (title, author, genre, stock_qty, price)
    VALUES (@book_title, @book_author, @genre, @stock_qty, @price)
RETURN 0;
GO

-- ============================================================
-- PROSEDURALAR: BUYURTMALAR
-- ============================================================

CREATE PROCEDURE dbo.GetUserOrders
    @user_name varchar(35)
AS
    SELECT id, dbo.InitCap(@user_name) AS user_name, total_amount, status FROM orders
    WHERE user_id IN (
        SELECT id FROM users
        WHERE LOWER(name) = LOWER(@user_name)
    ) AND status = 'completed'
RETURN 0;
GO

CREATE PROCEDURE dbo.get_user_orders
    @user_email varchar(45)
AS
    SELECT id, total_amount, status, ordered_at FROM orders
    WHERE user_id = (
        SELECT id FROM users
        WHERE email = @user_email
    )
RETURN 0;
GO

CREATE PROCEDURE dbo.get_user_p_orders
    @user_email varchar(45)
AS
    SELECT id, total_amount, status, ordered_at FROM orders
    WHERE status = 'pending' AND user_id = (
        SELECT id FROM users
        WHERE email = @user_email
    )
RETURN 0;
GO

CREATE PROCEDURE dbo.cancel_orders
    @product_id int
AS
    UPDATE orders
    SET status = 'cancelled'
    WHERE id = @product_id
RETURN 0;
GO

-- ============================================================
-- TRIGGER: buyurtma elementi qo'shilganda zaxira logi yoziladi
-- ============================================================

CREATE TRIGGER trg_insert_inventory_log
ON order_items
AFTER INSERT
AS
BEGIN
    INSERT INTO inventory_logs (book_id, change_qty, reason, changed_at)
    SELECT book_id, -quantity, 'Sale', GETDATE()
    FROM inserted
END;
GO

-- ============================================================
-- VIEWLAR
-- ============================================================

CREATE VIEW dbo.view_top_books
AS
WITH cte AS (
    SELECT TOP 1 WITH TIES * FROM order_items
    ORDER BY quantity
), cte_2 AS (
    SELECT book_id, SUM(quantity) AS sum FROM cte
    GROUP BY book_id
), cte_3 AS (
    SELECT TOP 1 WITH TIES book_id FROM cte_2
    ORDER BY sum DESC
)
SELECT id, title, author, genre, stock_qty, price FROM books
WHERE id IN (SELECT * FROM cte_3);
GO

CREATE VIEW dbo.select_top_buyers
AS
WITH cte AS (
    SELECT s1.id, status, ordered_at, s5.price FROM users s1
    JOIN orders s2 ON s1.id = s2.user_id
    JOIN inventory_logs s3 ON s2.id = s3.id
    JOIN order_items s4 ON s2.id = s4.book_id
    JOIN books s5 ON s4.book_id = s5.id
    WHERE ordered_at BETWEEN DATEADD(MONTH, -1, GETDATE()) AND GETDATE()
), cte2 AS (
    SELECT TOP 2 WITH TIES id, COUNT(status) AS cnt FROM cte
    GROUP BY id
    ORDER BY cnt DESC
)
SELECT s2.id, s2.name, s2.email, s2.phone, cnt AS orders_count
FROM cte2 s1
JOIN users s2 ON s1.id = s2.id;
GO