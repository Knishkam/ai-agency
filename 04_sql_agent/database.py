import sqlite3 
import os
from datetime import datetime
from pathlib import Path
DATABASE_PATH = Path("company.db")
def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEST UNIQUE,
        city TEXT,
        total_purchases REAL DEFAULT 0
    )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 100
    )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEFER,
            quantity INTEGER DEFAULT 1,
            amout REAL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
def insert_sample_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELEte FROM products")
    customers = [
        ("Rahul Sharma", "rahul@example.com", "Delhi", 15000.50),
        ("Priya Singh", "priya@example.com", "Mumbai", 25000.00),
        ("Amit Kumar", "amit@example.com", "Bangalore", 8000.75),
        ("Sunita Devi", "sunita@example.com", "Chennai", 32000.00),
        ("Vikram Patel", "vikram@example.com", "Hyderabad", 18500.25),
        ("Neha Gupta", "neha@example.com", "Kolkata", 12000.00),
        ("Ravi Verma", "ravi@example.com", "Delhi", 9500.00),
    ]
    cursor.executemany(
        "INSERT INTO customers (name, email, city, total_purchases) VALUES (?, ?, ?, ?)",
        customers
        )
    products = [
        ("Laptop", "Electronics", 75000.00, 50),
        ("Smartphone", "Electronics", 15000.00, 200),
        ("Headphones", "Accessories", 2000.00, 300),
        ("Office Chair", "Furniture", 5000.00, 100),
        ("Coffee Maker", "Appliances", 3000.00, 80),
        ("Running Shoes", "Footwear", 4000.00, 150),
        ("Backpack", "Accessories", 2500.00, 120),
    ]
    cursor.executemany(
        "INSERT INTO products (product_name, category, price, stock) VALUES (?, ?, ?, ?)",
        products
        )
    orders = [
        (1, 1, 1, 15000.00),
        (2, 2, 2, 30000.00),
        (3, 3, 1, 7500.00),
        (4, 4, 3, 2000.00),
        (5, 5, 4, 5000.00),
        (6, 6, 5, 3000.00),
        (7, 7, 6, 4000.00),
    ]
    cursor.executemany(
        "INSERT INTO orders (customer_id, product_id, quantity, amout) VALUES (?, ?, ?, ?)",
        orders
        )
    conn.commit()
    conn.close()
    print("Database created and sample data inserted successfully!")
if __name__ == "__main__":
    create_database()
    insert_sample_data()