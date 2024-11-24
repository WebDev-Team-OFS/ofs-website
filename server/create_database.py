import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash



#update password to whatever you set your msql password to
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminpass",   #change if you set password   
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
    email VARCHAR(100) UNIQUE,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

#admin table
# cursor.execute("""
# CREATE TABLE IF NOT EXIST admin_info (
#     emp_id INT AUTO_INCREMENT PRIMARY KEY, 
#     username VARCHAR(50),
#     password VARCHAR(255),
#     first_name VARCHAR(50),
#     last_name VARCHAR(50),
#     email VARCHAR(100) UNIQUE,
#     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )                       
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_info (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
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
    category VARCHAR(50),
    description TEXT,
    image LONGBLOB
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_price DECIMAL(10, 2),
    total_weight DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_items JSON
    -- FOREIGN KEY (user_id) REFERENCES user_info(user_id),
)
""")

#create cart table


#remove if nont being used 
cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    user_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES user_info(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
    )
""")



user_password = generate_password_hash("pass123")
# Insert test data into user_info
test_users = [
    ("john123", user_password, "John", "Doe", "john@example.com"),
    ("bobbyL", "loxd", "Bobby", "Lee", "bobby@example.com"),
    ("bjorkM", "vespertine", "Bjork", "Magnusson", "bjork@example.com")
]

cursor.executemany("INSERT INTO user_info (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)", test_users)
mydb.commit()

admin_password = generate_password_hash("adminpass");
test_admin = [
    ("adminUser", admin_password, "Admin", "User", "admin@example.com"),
    ("employee1", "emppass", "employee1", "User", "employee1@example.com"),
]
cursor.executemany("INSERT INTO admin_info (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)", test_admin)
mydb.commit()




# Insert test data into product (with category and placeholder for image)
test_products = [
    ("Organic Apples", "NatureFresh", 0, 1.39, 1.0, True, "Produce", "Apples are a crisp, refreshing fruit packed with natural sweetness and a satisfying crunch. Rich in fiber and vitamin C, they make a healthy snack that's perfect for any time of day. Enjoy them whole, sliced, or added to salads, desserts, and recipes. With a variety of flavors from sweet to tart, apples are a versatile and nutritious choice for everyone!", "images/apple.png"),
    ("Almond Milk", "Silk", 5, 3.49, 1.0, True, "Dairy", "Indulge in the rich, smooth taste of Silk Organic Original Almond Milk. Carefully crafted from high-quality organic almonds, this plant-based milk alternative is certified USDA Organic and packed with natural goodness. With only 50 calories per serving, it offers a creamy, delicious flavor perfect for your morning cereal, smoothies, coffee, or just by itself.", "images/almondmilk.png"),
    ("Whole Grain Bread", "Baker's Choice", 75, 2.99, 0.8, True, "Grains", "Whole wheat bread is a wholesome, hearty option made from 100% whole grains, offering a rich source of fiber and essential nutrients. Its nutty flavor and soft texture make it perfect for sandwiches, toast, or pairing with soups and salads. Packed with vitamins, minerals, and complex carbohydrates, whole wheat bread is a nutritious choice for a balanced diet.", "images/whole_grain.png"),
    ("Baby Carrots", "Kroger", 75, 2.99, 0.8, True, "Produce", "Baby carrots are a convenient and healthy snack, naturally sweet and bite-sized for easy munching. Perfect for salads, lunchboxes, or on-the-go, they are rich in vitamins A and C, supporting vision and immune health. Pre-washed and ready to eat, baby carrots are a fresh, crunchy choice for any occasion!", "images/baby_carrot.jpg"),
    ("Whole wheat Bread", "Dave's Killer", 75, 2.99, 0.8, True, "Grains", "Fuel your day with the hearty, nutritious goodness of Dave's Killer Bread 21 Whole Grains and Seeds. Each slice is packed with a rich blend of organic whole grains and seeds, providing a robust flavor and a satisfying crunch. Perfect for sandwiches, toast, or as a standalone snack, this bread is not only delicious but also loaded with essential nutrients to keep you energized throughout the day.", "images/daves_bread.png"),
    ("Chocolate Chip Cookies", "Entenmann's", 75, 2.99, 0.8, True, "Snacks", "Mini chocolate cookies are bite-sized treats packed with rich, chocolaty goodness. Crispy on the outside and soft in the middle, they offer the perfect balance of sweetness in every bite. Ideal for snacking, sharing, or adding a sweet touch to any occasion, these mini cookies are a delicious indulgence for chocolate lovers!.", "images/chocolate_chip_cookies.png"),
    ("Large Farm Eggs", "Kirkland", 75, 2.99, 0.8, True, "Produce", "A dozen eggs are a versatile kitchen staple, rich in high-quality protein, vitamins, and minerals. Perfect for breakfast, baking, or adding to your favorite recipes, eggs are a nutritious and convenient ingredient. Whether scrambled, boiled, or fried, they provide endless meal possibilities and essential nutrients for a balanced diet.", "images/eggs.png"),
    ("Lunchly Fiesta Nachos with Prime", "Mr. Beast's", 75, 2.99, 0.8, True, "Snacks", "Lunchly is a convenient meal solution designed to make lunchtime easy and delicious. With a variety of wholesome, ready-to-eat options, Lunchly offers balanced meals that fit into your busy day. Whether you're craving fresh salads, hearty sandwiches, or protein-packed bowls, Lunchly provides nutritious and satisfying choices for every taste. Ideal for work, school, or on-the-go, Lunchly makes lunchtime simple, healthy, and enjoyable!", "images/lunchly.png"),
    ("Dairy Free Plain Yogurt", "Kirckland", 75, 2.99, 0.8, True, "Dairy", "Vanilla yogurt (32 oz) is a creamy, delicious treat with the perfect hint of natural vanilla flavor. Packed with live and active cultures, it's a great source of probiotics for gut health. Rich in protein and calcium, this smooth and versatile yogurt is perfect on its own, blended into smoothies, or topped with fruits and granola for a wholesome snack. The 32 oz container is ideal for sharing or enjoying throughout the week!", "images/Kirkland_Greek_Yogurt.jpeg"),
    ("Prime Hydration", "KSI", 75, 2.99, 0.8, True, "Drinks", "Prime Hydration is a refreshing drink designed to keep you hydrated and energized throughout the day. With a blend of electrolytes, antioxidants, and B vitamins, it supports optimal hydration while boosting your energy levels. Whether you're working out, recovering, or just staying active, Prime Hydration provides the perfect balance of hydration and replenishment without added sugar. Stay refreshed and revitalized with every sip!", "images/prime.jpeg"),
    ("Chicken Noodle Soup", "Progresso", 75, 2.99, 0.8, False, "Canned Foods", "Progresso Chicken Noodle Soup is a comforting, ready-to-eat classic made with tender white meat chicken, hearty noodles, and a flavorful broth. Perfect for a quick and satisfying meal, it's packed with quality ingredients and rich, savory taste. Whether you're warming up on a chilly day or craving a comforting lunch, Progresso Chicken Noodle Soup offers a delicious, no-fuss solution that's ready in minutes!", "images/chicken_noodles.png"),
    ("Takis", "Great Value", 75, 2.99, 0.8, False, "Snack", "Takis are bold, crunchy rolled tortilla chips with an intense kick of spice and tangy flavor. Each bite packs a punch, offering an unforgettable experience for snack lovers who crave something fiery and flavorful. Known for their distinctive shape and zesty seasoning, Takis are perfect for anyone looking for a snack with an extra edge. Ideal for sharing (or not!), these chips bring a burst of excitement to any snack time.", "images/takis.jpeg"),
    ("Chicken breast", "Foster Farms", 75, 2.99, 0.8, False, "Meats", "Enjoy premium, high-quality chicken with Foster Farms Organic Free Range Chicken Breast Fillets. These boneless, skinless breast fillets are sourced from free-range chickens raised on organic vegetarian feed, ensuring a pure and natural taste. The chicken is air-chilled, meaning no water is added during processing, preserving the natural texture and flavor of the meat.", "images/chicken_breast.jpeg"),
    ("Tomato Paste", "Hunts", 75, 2.99, 0.8, False, "Canned Food", "Create rich, flavorful dishes with Hunt's 100% Natural Tomato Paste. Made from carefully selected, vine-ripened tomatoes, this paste brings bold, robust tomato flavor to any recipe. Perfect for enhancing pasta sauces, soups, stews, and more, it's a versatile pantry staple that helps elevate your cooking with its concentrated, authentic taste.", "images/tomate_paste.png"),
    ("Ghost Sour Pink Lemonade Energy Drink", "Ghost", 75, 2.99, 0.8, False, "Drinks", "Power up your day with a refreshing twist from GHOST Energy - Sour Pink Lemonade. This energy drink offers a unique, tangy lemonade flavor designed to invigorate your taste buds while providing a clean energy boost. With zero sugar and no artificial colors, GHOST Energy is formulated to fuel your active lifestyle without the unwanted crash.", "images/ghost_drink.png"),
    ("Turkey Breast Lunch Meat", "Foster Farms", 75, 2.99, 0.8, False, "Meats", "Elevate your sandwiches and salads with the delightful taste of Foster Farms Honey Roasted Turkey Breast. Made from premium cuts of turkey breast, this lunch meat is infused with a hint of honey for a subtly sweet flavor that pairs perfectly with any meal. Crafted with care, it contains no added nitrates, nitrites, or artificial flavors, making it a healthier choice for your daily protein needs.", "images/FF_turkey_breast.jpg"),
    ("Laura's Ground Beef", "Laura's Lean Beef", 75, 2.99, 0.8, False, "Meats", "Enjoy guilt-free meals with Laura's Lean 96% Lean Ground Beef. This high-quality ground beef is sourced from cattle raised without antibiotics or added hormones, ensuring a natural and nutritious option for your favorite recipes. With only 4% fat, it offers a leaner alternative that still delivers rich, hearty flavor without the extra calories.", "images/lauras_beef.png"),
    ("Guerrero Tortilla", "Guerrero", 75, 5.99, 0.8, False, "Grains", "Bring authentic Mexican flavor to your table with Guerrero Riquísimas Soft Taco Flour Tortillas. These tortillas are crafted to be soft, flexible, and perfect for making delicious tacos, wraps, and quesadillas. With a rich and traditional taste, they're ideal for adding a homemade touch to your meals and are designed to stay fresh and pliable for any dish.", "images/tortilla.png"),
    ("Bush's Baked Beans ", "Bush's", 75, 3.99, 0.8, False, "Canned food", "Enjoy the classic taste of Bush's Best Original Baked Beans, slow-cooked to perfection with a delicious blend of flavors. Infused with real bacon and brown sugar, these beans offer a rich, smoky-sweet taste that complements any meal, from barbecues to hearty dinners. With Bush's secret family recipe, every bite brings wholesome goodness and unmatched flavor.", "images/bush_beans.png"),
    ("Daisy Sour Cream", "Daisy", 75, 4.99, 0.8, False, "Grains", "Enhance your favorite dishes with the creamy, rich taste of Daisy Sour Cream. Made with just one simple, natural ingredient, this sour cream delivers a pure, smooth texture that's perfect for dolloping onto tacos, baked potatoes, or incorporating into dips and recipes. Trusted for its consistency and fresh flavor, Daisy brings a touch of quality to every meal.", "images/Daisy_sour_cream.jpeg"),
    ("Pringles Sour Cream and Onion", "Pringles", 75, 2.50, 0.8, False, "Grains", "Satisfy your snack cravings with the bold and zesty flavor of Pringles Sour Cream & Onion. These iconic, stackable potato crisps offer the perfect blend of tangy sour cream and savory onion, delivering a taste that's impossible to resist. Packaged in the signature resealable can, Pringles ensures your chips stay fresh and crunchy from the first bite to the last.", "images/sour_cream_pringles.jpg"),
    ("Cayanne Pepper", "Simply Organic", 75, 2.99, 0.8, False, "Ingredients", "Add a fiery kick to your favorite dishes with Simply Organic Cayenne Pepper. This high-quality spice is made from pure, organic cayenne peppers, providing a bold, hot flavor that enhances soups, sauces, meats, and more. Perfect for those who enjoy a touch of heat, this cayenne pepper is USDA Organic certified, ensuring it meets the highest standards of quality and sustainability.", "images/cayenne_pepper.png"),
    ("Azumaya Tofu", "Azumaya", 25, 2.99, 1.0, True, "Produce", "Enjoy the versatility and nutritional benefits of Azumaya Firm Tofu, a perfect plant-based protein option for any meal. This firm tofu is made with non-GMO soybeans and is an excellent source of calcium, making it a healthy addition to stir-fries, soups, salads, and more. With its firm texture, it holds up well to cooking, grilling, and frying, making it ideal for a variety of culinary creations.", "images/tofu.jpeg"),
    ("Kraft Original Cheese Slices", "Kraft", 75, 4.99, 0.75, True, "Dairy", "Add a rich, creamy taste to your sandwiches and burgers with Kraft Original Cheese Slices. Made to melt perfectly, these slices offer the classic, beloved flavor of Kraft cheese that generations have enjoyed. With 10 individually wrapped slices, they're ideal for quick, easy use and stay fresh until you're ready to enjoy them.", "images/kraft_cheese.jpeg"),
    ("Chicken breast", "Foster Farms", 75, 2.99, 0.8, False, "Grains", "Freshly baked whole grain bread.", None),
    ("Chicken breast", "Foster Farms", 75, 2.99, 0.8, False, "Grains", "Freshly baked whole grain bread.", None),
    ("Chicken breast", "Foster Farms", 75, 2.99, 0.8, False, "Grains", "Freshly baked whole grain bread.", None),


]

cursor.executemany("INSERT INTO product (name, brand, stock, price, weight, featured, category, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", test_products)
mydb.commit()

# Insert test data into orders
# test_orders = [
#     (1, 2, 5.98, "2024-10-01 10:30:00", 1),
#     (2, 1, 6.98, "2024-10-02 12:45:00", 2)
# ]

# cursor.executemany("INSERT INTO orders (user_id, amount, cost, order_date, product_id) VALUES (%s, %s, %s, %s, %s)", test_orders)
# mydb.commit()

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

# Retrieve and display cart data
cursor.execute("SELECT * FROM cart")
for order in cursor.fetchall():
    print(order)
    

cursor.close()
mydb.close()
