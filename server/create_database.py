import mysql.connector


#update password to whatever you set your msql password to
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminpass",#change if you set password   
    auth_plugin = 'mysql_native_password'
)

cursor = mydb.cursor()


# Create and use the 'ofs_database' database
cursor.execute("CREATE DATABASE IF NOT EXISTS ofs_database")
cursor.execute("USE ofs_database")

# Create user_info table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_info (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    is_admin BOOLEAN DEFAULT 0,  # This column indicates if a user is an admin (1 for admin, 0 for non-admin)
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    brand VARCHAR(100),
    stock INT,
    price DECIMAL(10, 2),
    weight DECIMAL(5, 2),
    featured BOOLEAN,
    description TEXT
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_number INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount INT,
    cost DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_id INT,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
)
""")



# Create image table
cursor.execute("""
CREATE TABLE IF NOT EXISTS image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    image LONGBLOB,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
)
""")

# Insert test data into user_info
test_users = [
    ("john123", "pass123", "John", "Doe", "john@example.com",0),
    ("bobbyL", "loxd", "Bobby", "Lee", "bobby@example.com",0),
    ("bjorkM", "vespertine", "Bjork", "Magnusson", "bjork@example.com",0),
    ("adminUser", "adminpass", "Admin", "User", "admin@example.com", 1)
]

cursor.executemany("INSERT INTO user_info (username, password, first_name, last_name, email, is_admin) VALUES (%s, %s, %s, %s, %s, %s)", test_users)
mydb.commit()

# Insert test data into product
test_products = [
    ("Organic Apples", "NatureFresh", 100, 1.99, 0.5, True, "Crisp and fresh organic apples."),
    ("Almond Milk", "NutriFarm", 50, 3.49, 1.0, False, "Non-dairy almond milk."),
    ("Whole Grain Bread", "Baker's Choice", 75, 2.99, 0.8, False, "Freshly baked whole grain bread.")
]

cursor.executemany("INSERT INTO product (name, brand, stock, price, weight, featured, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", test_products)
mydb.commit()

# Insert test data into orders
test_orders = [
    (1, 2, 5.98, "2024-10-01 10:30:00", 1),
    (2, 1, 6.98, "2024-10-02 12:45:00", 2)
]

cursor.executemany("INSERT INTO orders (user_id, amount, cost, order_date, product_id) VALUES (%s, %s, %s, %s, %s)", test_orders)
mydb.commit()

#These scripts will be need to be updated by the backend team 
#is there are extra commands we need a extra file to call upon this so make another file for just user calls
#This will be to create the data base only


# Retrieve and display user data
cursor.execute("SELECT * FROM user_info")
for user in cursor.fetchall():
    print(user)

# Retrieve and display product data
cursor.execute("SELECT * FROM product")
for product in cursor.fetchall():
    print(product)

# Retrieve and display order data
cursor.execute("SELECT * FROM orders")
for order in cursor.fetchall():
    print(order)

cursor.close()
mydb.close()