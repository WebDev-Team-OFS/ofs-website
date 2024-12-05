import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import time
import os

for _ in range(10):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'adminpass'),#change password here
            auth_plugin='mysql_native_password'
        )
        break
    except Error:
        print("Waiting for database connection...")
        time.sleep(5)
else:
    print("Could not connect to the database.")
    exit(1)


#lastest db update 11/25/2024

#update password to whatever you set your msql password to
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "adminpass",   #change if you set password   
#     auth_plugin = 'mysql_native_password'
# )

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
("Prime Hydration", "KSI", 75, 2.99, 0.8, True, "Drinks", "Prime Hydration is a refreshing drink designed to keep you hydrated and energized throughout the day. With a blend of electrolytes, antioxidants, and B vitamins, it supports optimal hydration while boosting your energy levels. Whether you're working out, recovering, or just staying active, Prime Hydration provides the perfect balance of hydration and replenishment without added sugar. Stay refreshed and revitalized with every sip!", "images/prime.jpeg"),
("Chicken Noodle Soup", "Progresso", 75, 2.99, 0.8, True, "Canned Foods", "Progresso Chicken Noodle Soup is a comforting, ready-to-eat classic made with tender white meat chicken, hearty noodles, and a flavorful broth. Perfect for a quick and satisfying meal, it's packed with quality ingredients and rich, savory taste. Whether you're warming up on a chilly day or craving a comforting lunch, Progresso Chicken Noodle Soup offers a delicious, no-fuss solution that's ready in minutes!", "images/chicken_noodles.png"),
("Takis", "Great Value", 75, 2.99, 0.8, True, "Snacks", "Takis are bold, crunchy rolled tortilla chips with an intense kick of spice and tangy flavor. Each bite packs a punch, offering an unforgettable experience for snack lovers who crave something fiery and flavorful. Known for their distinctive shape and zesty seasoning, Takis are perfect for anyone looking for a snack with an extra edge. Ideal for sharing (or not!), these chips bring a burst of excitement to any snack time.", "images/takis.jpeg"),
("Chicken breast", "Foster Farms", 75, 2.99, 0.8, True, "Meats", "Enjoy premium, high-quality chicken with Foster Farms Organic Free Range Chicken Breast Fillets. These boneless, skinless breast fillets are sourced from free-range chickens raised on organic vegetarian feed, ensuring a pure and natural taste. The chicken is air-chilled, meaning no water is added during processing, preserving the natural texture and flavor of the meat.", "images/chicken_breast.jpeg"),
("Tomato Paste", "Hunts", 75, 2.99, 0.8, False, "Canned Foods", "Create rich, flavorful dishes with Hunt's 100% Natural Tomato Paste. Made from carefully selected, vine-ripened tomatoes, this paste brings bold, robust tomato flavor to any recipe. Perfect for enhancing pasta sauces, soups, stews, and more, it's a versatile pantry staple that helps elevate your cooking with its concentrated, authentic taste.", "images/tomato_paste.png"),
("Sour Pink Lemonade Energy Drink", "Ghost", 75, 2.99, 0.8, False, "Drinks", "Power up your day with a refreshing twist from GHOST Energy - Sour Pink Lemonade. This energy drink offers a unique, tangy lemonade flavor designed to invigorate your taste buds while providing a clean energy boost. With zero sugar and no artificial colors, GHOST Energy is formulated to fuel your active lifestyle without the unwanted crash.", "images/ghost_drink.png"),
("Turkey Breast Lunch Meat", "Foster Farms", 75, 2.99, 0.8, False, "Meats", "Elevate your sandwiches and salads with the delightful taste of Foster Farms Honey Roasted Turkey Breast. Made from premium cuts of turkey breast, this lunch meat is infused with a hint of honey for a subtly sweet flavor that pairs perfectly with any meal. Crafted with care, it contains no added nitrates, nitrites, or artificial flavors, making it a healthier choice for your daily protein needs.", "images/FF_turkey_breast_lunch_meat.jpg"),
("Laura's Ground Beef", "Laura's Lean Beef", 75, 2.99, 0.8, False, "Meats", "Enjoy guilt-free meals with Laura's Lean 96% Lean Ground Beef. This high-quality ground beef is sourced from cattle raised without antibiotics or added hormones, ensuring a natural and nutritious option for your favorite recipes. With only 4% fat, it offers a leaner alternative that still delivers rich, hearty flavor without the extra calories.", "images/laura_ground_beef.png"),
("Tortillas", "Guerrero", 75, 5.99, 0.8, False, "Grains", "Bring authentic Mexican flavor to your table with Guerrero Riquísimas Soft Taco Flour Tortillas. These tortillas are crafted to be soft, flexible, and perfect for making delicious tacos, wraps, and quesadillas. With a rich and traditional taste, they're ideal for adding a homemade touch to your meals and are designed to stay fresh and pliable for any dish.", "images/tortillas.png"),
("Baked Beans ", "Bush's", 75, 3.99, 0.8, False, "Canned Foods", "Enjoy the classic taste of Bush's Best Original Baked Beans, slow-cooked to perfection with a delicious blend of flavors. Infused with real bacon and brown sugar, these beans offer a rich, smoky-sweet taste that complements any meal, from barbecues to hearty dinners. With Bush's secret family recipe, every bite brings wholesome goodness and unmatched flavor.", "images/bush_beans.png"),
("Sour Cream", "Daisy", 75, 4.99, 0.8, False, "Dairy", "Enhance your favorite dishes with the creamy, rich taste of Daisy Sour Cream. Made with just one simple, natural ingredient, this sour cream delivers a pure, smooth texture that's perfect for dolloping onto tacos, baked potatoes, or incorporating into dips and recipes. Trusted for its consistency and fresh flavor, Daisy brings a touch of quality to every meal.", "images/Daisy_sour_cream.jpeg"),
("Sour Cream and Onion Chips", "Pringles", 75, 2.50, 0.8, False, "Snacks", "Satisfy your snack cravings with the bold and zesty flavor of Pringles Sour Cream & Onion. These iconic, stackable potato crisps offer the perfect blend of tangy sour cream and savory onion, delivering a taste that's impossible to resist. Packaged in the signature resealable can, Pringles ensures your chips stay fresh and crunchy from the first bite to the last.", "images/sour_cream_pringles.jpg"),
("Cayanne Pepper", "Simply Organic", 75, 2.99, 0.8, False, "Ingredients", "Add a fiery kick to your favorite dishes with Simply Organic Cayenne Pepper. This high-quality spice is made from pure, organic cayenne peppers, providing a bold, hot flavor that enhances soups, sauces, meats, and more. Perfect for those who enjoy a touch of heat, this cayenne pepper is USDA Organic certified, ensuring it meets the highest standards of quality and sustainability.", "images/cayanne_pepper.png"),
("Tofu", "Azumaya", 25, 2.99, 1.0, False, "Produce", "Enjoy the versatility and nutritional benefits of Azumaya Firm Tofu, a perfect plant-based protein option for any meal. This firm tofu is made with non-GMO soybeans and is an excellent source of calcium, making it a healthy addition to stir-fries, soups, salads, and more. With its firm texture, it holds up well to cooking, grilling, and frying, making it ideal for a variety of culinary creations.", "images/tofu.jpeg"),
("Cheese Slices", "Kraft", 75, 4.99, 0.75, False, "Dairy", "Add a rich, creamy taste to your sandwiches and burgers with Kraft Original Cheese Slices. Made to melt perfectly, these slices offer the classic, beloved flavor of Kraft cheese that generations have enjoyed. With 10 individually wrapped slices, they're ideal for quick, easy use and stay fresh until you're ready to enjoy them.", "images/kraft_cheese.jpg"),
("Pepsi 20 OZ Bottle", "Pepsi", 500, 1.99, 1.25, False, "Drinks ", "Refresh yourself with the classic, crisp taste of Pepsi. This 500ml bottle is the perfect size for on-the-go enjoyment or a quick refreshment at home. With its bold flavor and just the right amount of sweetness, Pepsi has been a favorite for generations. Enjoy it chilled for maximum refreshment.", "images/pepsi.png"),
("Coca-Cola 24 OZ Bottle", "Coca-Cola", 591, 1.89, 1.5, False, "Drinks", "Experience the timeless and refreshing taste of Coca-Cola. This 591ml bottle is the perfect size for enjoying the iconic cola flavor you love, whether on the go or at home. Perfectly balanced with a crisp and invigorating taste, Coca-Cola remains a favorite around the world. Enjoy it chilled for maximum satisfaction.", "images/coke.png"),
("Monster Energy 16oz Can", "Monster", 563, 2.49, 1.05, False, "Drinks", "Unleash the beast with Monster Energy! This 16oz can delivers a powerful punch of energy and a smooth, refreshing taste. Packed with a unique blend of ingredients and a bold flavor, Monster Energy is perfect for fueling your day or pushing through your limits. Enjoy it chilled for the ultimate energy boost.", "images/monster.png"),
("Smartwater 1L Bottle (Case of 24)", "Smartwater", 45, 19.99, 26.4, False, "Drinks", "Hydrate intelligently with Smartwater. This case of 24 1L bottles offers crisp, vapor-distilled water with added electrolytes for a refreshing and pure taste. Perfect for staying hydrated throughout the day, Smartwater is the ideal choice for a healthy and balanced lifestyle. Enjoy the convenience of this bulk pack for home or office.", "images/water.png"),
("Sprite 1.25L Bottle", "Sprite", 150, 1.99, 2.76, False, "Drinks", "Enjoy the refreshing and crisp taste of Sprite. This 1.25L bottle is perfect for sharing or savoring on your own. With its iconic lemon-lime flavor and caffeine-free formula, Sprite is a great choice for any occasion. Serve it chilled to quench your thirst and brighten your day.", "images/sprite.png"),
("Red Bull Energy Drink 8.4oz Can", "Red Bull", 250, 2.49, 0.55, False, "Drinks", "Fuel your energy with Red Bull Energy Drink. This 8.4oz can is packed with caffeine, taurine, and essential B-vitamins to help you stay alert and focused. With its lightly carbonated, classic flavor, Red Bull is perfect for powering through busy days or late-night challenges. Serve chilled for maximum refreshment.", "images/redbull.png"),
("Reign Total Body Fuel 16oz Can ", "Reign", 473, 2.99, 1.05, False, "Drinks", "Fuel your workout and power through the day with Reign Total Body Fuel. This 16oz can is packed with BCAAs, CoQ10, electrolytes, and 300mg of natural caffeine for sustained energy. With zero sugar and a bold, refreshing taste, Reign is your ultimate fitness-focused energy drink. Serve chilled for optimal enjoyment.", "images/reign.png"),
("Fanta Orange 12oz Can", "Fanta", 355, 1.49, 0.78, False, "Drinks", "Brighten your day with the vibrant and refreshing taste of Fanta Orange. This 12oz can delivers a burst of sweet and tangy orange flavor made with 100% natural flavors. Perfect for any occasion, Fanta Orange is caffeine-free and ideal for enjoying with meals or as a stand-alone treat. Serve chilled for the ultimate refreshment.", "images/fanta.png"),
("Alani Nu Energy Drink 12oz Can - Cherry Slush", "Alani Nu", 355, 2.29, 0.78, False, "Drinks", "Boost your energy with the fun and refreshing flavor of Alani Nu Cherry Slush. This 12oz can is packed with 200mg of caffeine to power your day, while being sugar-free and filled with bold cherry flavor. Perfect for a pre-workout boost or an afternoon pick-me-up, this lightly carbonated drink is a delicious way to stay energized. Serve chilled for maximum enjoyment.", "images/alani.png"),
("C4 Energy Drink 16oz Can - Hawaiian Pineapple", "C4", 473, 2.49, 1.05, False, "Drinks", "Fuel your workout with the tropical taste of C4 Energy Drink in Hawaiian Pineapple flavor. This 16oz can delivers zero sugar, 200mg of caffeine, and performance-enhancing ingredients to help you push past your limits. Perfect for athletes and fitness enthusiasts, this energizing drink combines bold flavor with functional benefits. Serve chilled for maximum refreshment.", "images/c4.png"),
("Diet Dr Pepper 12oz Can", "Dr Pepper", 355, 1.49, 0.78, False, "Drinks", "Indulge in the classic and unique flavor of Dr Pepper with zero calories. This 12oz Diet Dr Pepper can offers the same bold, rich taste you love without the guilt. Perfect for those who want a refreshing beverage that fits their diet goals, it's caffeine-packed and wonderfully fizzy. Serve chilled for the ultimate enjoyment.", "images/dietdp.png"),
("Arizona Green Tea with Ginseng and Honey 22oz Can", "Arizona", 650, 1.29, 1.43, False, "Drinks", "Savor the refreshing taste of Arizona Green Tea with Ginseng and Honey. This 22oz can delivers a perfect blend of premium brewed green tea, natural honey, and ginseng for a smooth and invigorating flavor. A classic favorite, it's a great choice for staying hydrated and refreshed throughout the day. Serve chilled for the best experience.", "images/tea.png"),
("Celsius Sparkling Orange 12oz Can", "Celsius", 355, 2.29, 0.78, False, "Drinks", "Energize your body with Celsius Sparkling Orange. This 12oz can offers essential energy with 7 vitamins, minerals, and no sugar. Featuring a refreshing orange flavor and a sparkling finish, Celsius is the perfect choice for a pre-workout boost or an afternoon pick-me-up. Stay active and refreshed with this guilt-free energy drink. Serve chilled for best results.", "images/celsius.png"),
("Turkey & Cheddar Cracker Stackers", "Lunchables", 85, 2.99, 0.19, False, "Snacks", "Enjoy a fun and delicious snack with Lunchables Turkey & Cheddar Cracker Stackers. This convenient pack includes fresh slices of turkey, cheddar cheese, and crisp crackers, providing 13g of protein per serving. Perfect for school lunches, on-the-go snacking, or a quick bite at home. Guaranteed freshness and great taste in every bite.", "images/lunchables.png"),
("Flamin' Hot Crunchy Party Size", "Cheetos", 425, 4.99, 0.94, False, "Snacks", "Turn up the heat with Cheetos Flamin' Hot Crunchy in Party Size! This 15oz bag is packed with spicy, cheesy goodness that delivers a bold flavor and satisfying crunch. Perfect for sharing at parties or enjoying as a snack anytime, these fiery treats are sure to ignite your taste buds. Grab a bag and spice up your snacking game!", "images/hotcheetos.png"),
("Extra Butter Microwave Popcorn (6-Pack)", "Pop Secret", 522, 5.49, 1.15, False, "Snacks", "Enjoy movie night with the rich, buttery taste of Pop Secret Extra Butter Microwave Popcorn. This 6-pack offers the perfect blend of fluffy popcorn and extra buttery flavor in every bite. Easy to prepare and perfect for sharing, it's the ultimate snack for any occasion. Treat yourself to a warm, delicious bowl of popcorn today!", "images/popcorn.png"),
("Chocolate Bar", "Twix", 50, 1.49, 0.11, False, "Snacks", "Indulge in the irresistible combination of crunchy cookie, smooth caramel, and creamy milk chocolate with Twix. This single bar is perfect for satisfying your sweet tooth anytime, anywhere. Treat yourself to the classic, delectable flavor that has made Twix a favorite worldwide.", "images/twix.png"),
("5 Gum Spearmint Rain (35 Sticks)", "Wrigley's", 55, 2.99, 0.12, True, "Snacks", "Experience long-lasting freshness with Wrigley's 5 Gum Spearmint Rain. This pack includes 35 sticks of gum with a refreshing spearmint flavor that's perfect for keeping your breath fresh all day. Whether at work, school, or on the go, enjoy the cool and invigorating taste of 5 Gum.", "images/gum.png"),
("Fruit Adventure 24g", "Tic Tac", 24, 1.29, 0.05, False, "Snacks", "Embark on a flavorful journey with Tic Tac Fruit Adventure. This 24g pack features a mix of four fruity flavors in a convenient, pocket-sized container. Perfect for a quick refresh or a burst of sweetness on the go. Enjoy the fun, vibrant taste of Tic Tac Fruit Adventure anytime, anywhere.", "images/tictac.png"),
("12 Flavor Gummi Bears 7.5oz", "Albanese", 212, 3.49, 0.47, False, "Snacks", "Delight in the World's Best Gummi Bears with Albanese 12 Flavor Gummi Bears. This 7.5oz bag features a variety of delicious flavors, including cherry, pineapple, and watermelon, in soft, chewy gummies. Gluten-free, fat-free, and low sodium, these treats are perfect for satisfying your sweet tooth guilt-free. Share them or enjoy them all yourself!", "images/gummybear.png"),
("Sour Brite Crawlers Value Size 28.8oz", "Trolli", 816, 7.99, 1.8, False, "Snacks", "Indulge in the tangy and sweet flavors of Trolli Sour Brite Crawlers. This value-sized 28.8oz bag is packed with soft, chewy gummy worms coated in sour sugar for a mouth-puckering treat. Perfect for sharing or satisfying your own candy cravings, these colorful crawlers bring a burst of fun to every bite.", "images/trolli.png"),
("Mints Wintergreen 8-Pack", "Ice Breakers", 340, 8.49, 0.75, False, "Snacks", "Refresh your breath with Ice Breakers Wintergreen Mints. This 8-pack of 1.5oz tins features sugar-free mints infused with cooling crystals for a burst of freshness in every bite. Perfect for on-the-go moments, these mints are a convenient way to keep your breath fresh and your confidence high.", "images/mints.png"),
("Cheddar Cheese 156g Can", "Pringles", 156, 2.99, 0.34, False, "Snacks", "Satisfy your cheesy cravings with Pringles Cheddar Cheese. This 156g can offers perfectly stacked, crispy potato chips coated with bold cheddar cheese flavor. Whether for snacking at home or on the go, Pringles delivers consistent taste and crunch in every bite. Think outside the bag and grab a can today!", "images/cheddar pringle.png"),
("Cheddar & Sour Cream Party Size 12.5oz", "Ruffles", 354, 4.49, 0.78, False, "Snacks", "Enjoy the bold, savory flavor of Ruffles Cheddar & Sour Cream chips. This 12.5oz party-size bag is perfect for gatherings or satisfying your own snack cravings. With signature ridges for extra crunch, these chips are great for dipping or enjoying straight from the bag. Ruffles have ridges, and flavor you'll love!", "images/ruffles.png"),
("Sliced Ripe Olives 3.8oz", "Early California", 108, 1.79, 0.24, False, "Canned Foods", "Add a touch of Mediterranean flavor to your dishes with Early California Sliced Ripe Olives. This 3.8oz can features perfectly sliced California olives seasoned with sea salt. Great for salads, pizzas, or snacking, these non-GMO verified olives bring rich, savory taste to any meal.", "images/cannedolives.png"),
("Classic 12oz", "SPAM", 340, 3.49, 0.75, True, "Canned Foods", "Enjoy the iconic taste of SPAM Classic. This 12oz can is made with pork and ham, offering a versatile and convenient protein option for sandwiches, fried rice, or breakfast recipes. A pantry staple loved worldwide, SPAM is fully cooked and ready to eat.", "images/spam.png"),
("Fresh Cut French Style Green Beans 14.5oz", "Del Monte", 411, 1.29, 0.91, False, "Canned Foods", "Add fresh flavor to your meals with Del Monte Fresh Cut French Style Green Beans. This 14.5oz can features crisp, tender green beans grown in the USA and seasoned with sea salt. Perfect for side dishes, casseroles, or salads, these non-GMO beans are a nutritious and delicious addition to any meal.", "images/cannedgreenbeans.png"),
("Gold & White Corn 15.25oz", "Del Monte", 432, 1.49, 1.06, False, "Canned Foods", "Delight in the sweet and crisp taste of Del Monte Gold & White Corn. This 15.25oz can features whole kernel corn harvested at peak freshness and seasoned with natural sea salt. Perfect as a side dish or ingredient in soups, salads, and casseroles, it's a wholesome and non-GMO option for your pantry.", "images/cannedcorn.png"),
("100% Pure Pumpkin 15oz", "Libby's", 425, 2.89, 0.94, False, "Canned Foods", "Create delicious fall-inspired dishes with Libby's 100% Pure Pumpkin. This 15oz can contains all-natural, no-preservative pumpkin puree that's rich in Vitamin A. Perfect for pies, soups, or smoothies, this superfood adds wholesome goodness to every recipe.", "images/cannedpumpkin.png"),
("Pineapple Chunks in 100% Pineapple Juice 20oz", "Dole", 567, 2.49, 1.25, False, "Canned Foods", "Enjoy the tropical sweetness of Dole Pineapple Chunks in 100% Pineapple Juice. This 20oz can offers handpicked, perfectly ripe pineapple chunks with no added sugar. Great for recipes, snacking, or smoothies, these juicy fruits bring a taste of paradise to your day.", "images/cannedpineapple.png"),
("No Sugar Added Sliced Peaches 14.5oz", "Del Monte", 411, 1.79, 0.91, False, "Canned Foods", "Enjoy the fresh, juicy taste of Del Monte Sliced Peaches with no added sugar. Packed in water and lightly sweetened, this 14.5oz can is perfect for snacking, baking, or adding to salads. Non-GMO and naturally delicious, it's a healthy and convenient choice.", "images/cannedpeaches.png"),
("Chicken Broth 14.5oz", "Swanson", 411, 1.69, 0.91, False, "Canned Foods", "Elevate your cooking with Swanson Chicken Broth. This 14.5oz can of 100% natural, non-GMO broth delivers rich, savory flavor to soups, casseroles, and other dishes. A kitchen staple for home chefs everywhere.", "images/chickenbroth.png"),
("Chicken of the Sea Sardines in Water 3.75oz", "Chicken of the Sea", 106, 1.49, 0.23, False, "Canned Foods", "Savor the freshness of Chicken of the Sea Wild-Caught Sardines in Water. This 3.75oz can contains tender sardines with no added oil, making it a healthy and protein-rich option for snacks or meals. Perfect for sandwiches, salads, or straight out of the can.", "images/cannedsardines.png"),
("Jellied Cranberry Sauce 14oz", "Ocean Spray", 397, 2.49, 0.87, False, "Canned Foods", "Complete your holiday meals with Ocean Spray Jellied Cranberry Sauce. This 14oz can features the perfect blend of sweet and tangy cranberry flavor, making it a must-have side dish for Thanksgiving or any festive gathering.", "images/cannedcranberry.png"),
("Chopped Ocean Clams 51oz", "Snow's", 1440, 6.99, 3.17, False, "Canned Foods", "Add a taste of the sea to your recipes with Snow's Chopped Ocean Clams. This 51oz can is perfect for chowders, pasta dishes, or seafood soups. Wild-caught and packed in clam juice, these robust and firm clams offer a delicious and hearty flavor.", "images/cannedclams.png"),
("Smoked Oysters in Olive Oil 3oz", "Crown Prince", 85, 3.49, 0.19, False, "Canned Foods", "Enjoy gourmet flavor with Crown Prince Smoked Oysters. Hand-packed in olive oil, this 3oz can delivers rich, smoky taste perfect for appetizers, salads, or snacking. Non-GMO and sustainably sourced, these oysters are a delicious indulgence.", "images/cannedoyster.png"),
("Sourdough Bread", "Sourdough", 50, 4.99, 1.2, True, "Grains", "Indulge in the hearty and tangy flavor of freshly baked sourdough bread. Perfect for sandwiches or to enjoy with butter and jam, this loaf offers a delightful crust and soft interior, crafted from premium grains for a rich, satisfying taste.",  "images/sourdough.png"),
("Spaghetti", "Spaghetti", 100, 2.49, 1.0, False, "Grains",  "Enjoy classic Italian-style dining with Barilla Spaghetti. Made from 100% durum wheat semolina, this pasta cooks to an al dente perfection in just minutes, making it ideal for your favorite sauces and recipes.", "images/spaghetti.png"),
("Bobs Red Mill Rolled Oats", "Rolled Oats", 75, 5.99, 1.75, False, "Grains","Start your day with a healthy and hearty bowl of Bob’s Red Mill Rolled Oats. Packed with whole grain goodness, these oats are perfect for oatmeal, baking, or adding to your favorite recipes. Gluten-free and non-GMO.", "images/oatmeal.png"),
("Fettuccine", "Fettuccine", 80, 2.49, 1.0, False, "Grains", "Create delicious meals with Barilla Fettuccine, made from premium durum wheat semolina. This flat, ribbon-like pasta is perfect for creamy Alfredo sauces or rich tomato-based dishes.", "images/fettuccine.png"),
("Wonder Bread", "White Bread", 60, 2.99, 1.25, False, "Grains", "Experience the classic taste of Wonder Bread. Soft, fluffy, and fortified with essential nutrients, this white bread is ideal for sandwiches, toast, or your favorite recipes.", "images/whitebread.png"),
("B English Muffins", "English Muffins", 40, 3.99, 0.75, False, "Grains", "Soft and versatile Bays English Muffins are perfect for breakfast sandwiches or toasted with butter and jam. Made with high-quality ingredients, these muffins bring warmth to your morning routine.", "images/muffins.png"),
("All-Purpose Flour", "All-Purpose Flour", 50, 4.49, 5.0, False, "Grains", "King Arthur All-Purpose Flour is your go-to for all baking needs. Made from premium wheat, this unbleached flour is perfect for breads, pastries, and everything in between.", "images/flower.png"),
("Plain Bagels", "Plain Bagels", 30, 4.29, 1.25, False, "Grains", "Enjoy the chewy texture and rich flavor of Thomas’ Plain Bagels. Perfect for breakfast or a hearty snack, these bagels are pre-sliced for your convenience.", "images/bagels.png"),
("Jasmine Brown Rice", "Brown Rice", 25, 6.99, 5.0, False, "Grains", "Elevate your meals with Asian Best Jasmine Brown Rice. Nutty, aromatic, and wholesome, this premium-quality rice is ideal for stir-fries, curries, or as a nutritious side.", "images/brownrice.png"),
("Calrose Rice", "Calrose Rice", 20, 14.99, 15.0, False, "Grains", "Perfect for sushi, rice bowls, or any dish requiring soft, sticky rice, Botan Calrose Rice offers authentic flavor and quality with every grain.", "images/rice.png"),
("Pizza Crust", "Pizza Crust", 35, 3.59, 1.0, False, "Grains", "Craft your own pizza night with Pillsbury Pizza Crust. Easy to roll and bake, it provides a crispy yet tender base for your favorite toppings.", "images/pizzacrust.png"),
("Pie Crusts", "Pie Crusts", 40, 4.99, 1.25, False, "Grains", "Make baking easy with Pillsbury Pie Crusts. Flaky and buttery, these pre-made crusts save you time while delivering homemade flavor.", "images/piecrust.png"),
("USDA Choice Angus Top Sirloin", "Angus Sirloin", 25, 19.99, 1.5, False, "Meats", "USDA Choice Angus Top Sirloin steaks are tender and full of flavor, perfect for grilling or pan-searing. Enjoy the rich taste of high-quality beef.", "images/angussirloin.png"),
("Foster Farms Chicken Drumsticks", "Chicken Drumsticks", 40, 6.49, 3.0, False, "Meats", "Foster Farms Chicken Drumsticks are cage-free and 100% natural, offering juicy, flavorful chicken perfect for baking, grilling, or frying.", "images/chickenlegs.png"),
("Boneless Skinless Chicken Thighs", "Chicken Thighs", 35, 7.99, 2.5, False, "Meats", "Boneless and skinless chicken thighs are juicy and versatile, ideal for roasting, stir-fries, or slow cooking. A family favorite.", "images/chickenthigh.png"),
("Oscar Mayer Smoked Ham Lunchmeat", "Smoked Ham", 50, 4.29, 0.56, False, "Meats", "Oscar Mayer Smoked Ham lunchmeat is fresh, flavorful, and perfect for sandwiches or snacking. Gluten-free and free of artificial preservatives.", "images/hamlunchmeat.png"),
("Dino Buddies Chicken Nuggets", "Dino Nuggets", 30, 9.99, 2.375, False, "Meats", "Yummy Dino Buddies Chicken Nuggets are fun, dinosaur-shaped nuggets made with 100% natural chicken breast. Perfect for kids and adults alike.", "images/dinonugget.png"),
("Roasted Chicken Breast", "Chicken Lunchmeat", 40, 5.99, 0.44, False, "Meats", "Applegate Naturals Oven Roasted Chicken Breast is free of antibiotics and nitrates, making it a healthy and delicious option for sandwiches or wraps.", "images/chickenlunchmeat.png"),
("Choice Petite Filet Mignon", "Filet Mignon", 20, 29.99, 1.0, False, "Meats", "USDA Choice Petite Filet Mignon is tender and flavorful, making it perfect for special occasions or a gourmet dinner at home.", "images/filetmignon.png"),
("Hand-Trimmed Pork Chops", "Pork Chops", 30, 12.49, 2.0, False, "Meats", "Hand-selected and trimmed pork chops are juicy and flavorful, perfect for grilling, roasting, or pan-searing. A versatile dinner choice.", "images/porkchop.png"),
("Choice Bone-In Ribeye Steak", "Ribeye Steak", 20, 24.99, 1.25, False, "Meats", "USDA Choice Bone-In Ribeye Steak offers rich marbling and exceptional flavor. Perfect for grilling or pan-searing for a juicy, tender experience.", "images/ribeye.png"),
("Premium Pork Baby Back Ribs", "Baby Back Ribs", 15, 19.99, 5.0, False, "Meats", "Swift Premium Pork Baby Back Ribs are tender and meaty, ideal for slow cooking or barbecuing to perfection. A family favorite for gatherings.", "images/ribs.png"),
("Uncured Genoa Salami", "Genoa Salami", 50, 6.49, 0.25, False, "Meats", "Delallo Uncured Genoa Salami is all-natural with no nitrates or nitrites added. Perfect for charcuterie boards, sandwiches, or snacking.", "images/salami.png"),
("Fresh Broccoli Crowns", "Broccoli", 40, 2.99, 1.2, False, "Produce", "Fresh Broccoli Crowns are vibrant and nutrient-rich, perfect for steaming, roasting, or adding to your favorite dishes.", "images/broccoli.png"),
("Hass Avocado", "Avocado", 50, 1.49, 0.33, False, "Produce", "Hass Avocados are creamy and versatile, ideal for guacamole, salads, or spreading on toast for a healthy snack.", "images/avacado.png"),
("Red Bell Pepper", "Bell Pepper", 60, 1.99, 0.5, False, "Produce", "Red Bell Peppers are sweet and crisp, perfect for snacking, salads, or adding vibrant color to stir-fries.", "images/bellpepper.png"),
("Crisp Celery Stalks", "Celery", 30, 2.29, 1.25, False, "Produce", "Crisp Celery Stalks are refreshing and crunchy, great for dipping, soups, or as a healthy snack.", "images/celery.png"),
("Fresh Eggplant", "Eggplant", 25, 2.49, 1.5, False, "Produce", "Fresh Eggplant is tender and versatile, ideal for grilling, baking, or making a delicious eggplant parmesan.", "images/eggplant.png"),
("Juicy Lemons", "Lemons", 35, 0.79, 0.25, False, "Produce", "Juicy Lemons are zesty and fresh, perfect for cooking, baking, or squeezing into beverages.", "images/lemon.png"),
("Romaine Lettuce", "Lettuce", 40, 2.99, 1.0, False, "Produce", "Romaine Lettuce is crisp and refreshing, ideal for salads, wraps, or as a crunchy sandwich topping.", "images/lettuce.png"),
("Navel Oranges", "Oranges", 50, 1.29, 0.5, False, "Produce", "Navel Oranges are juicy and sweet, perfect for snacking or squeezing into fresh orange juice.", "images/orange.png"),
("Yellow Onions", "Onions", 45, 0.99, 0.8, False, "Produce", "Yellow Onions are flavorful and aromatic, a staple ingredient for soups, stews, and sautés.", "images/onion.png"),
("Green Bartlett Pears", "Pears", 30, 1.89, 0.5, False, "Produce", "Green Bartlett Pears are juicy and sweet, great for snacking, baking, or adding to salads.", "images/pear.png"),
("Mushrooms", "Mushrooms", 50, 2.99, 0.25, False, "Produce", "Fresh and earthy baby bella mushrooms, perfect for sautés and soups.", "images/mushrooms.png"),
("Original Dairy Whipped Topping", "Reddi Wip", 500, 3.49, 0.4, False, "Dairy", "Enhance your favorite desserts and beverages with the creamy, delicious taste of Reddi Wip Original Dairy Whipped Topping. Made with real cream, this 6.5 oz can provides a delightful, fluffy topping that's perfect for any treat. Elevate your strawberries, hot cocoa, and more with a dollop of Reddi Wip.", "images/whipcream.png"),
("Sliced Swiss Natural Cheese", "Brookshire's", 500, 2.99, 0.5, False, "Dairy", "Add a touch of sophistication to your sandwiches and snacks with Brookshire's Sliced Swiss Natural Cheese. This 8 oz package contains 10 slices of creamy and flavorful Swiss cheese, perfect for melting or enjoying as is. Rich in calcium and free from added sugars, it's a tasty and nutritious choice for your everyday meals. Keep refrigerated for optimal freshness.", "images/swiss.png"),
("Reduced Fat 2% Milk", "Great Value", 500, 3.49, 8.5, False, "Dairy", "Stay refreshed and healthy with Great Value Reduced Fat 2% Milk. This 1-gallon jug of milk offers 37% less fat than whole milk, making it a great choice for those looking to maintain a balanced diet. Enriched with vitamins A and D, and pasteurized for safety, this milk is perfect for drinking straight, pouring over cereal, or using in your favorite recipes.", "images/milk.png"),
("Natural Sliced Havarti Cheese", "Sargento", 500, 4.49, 0.44, False, "Dairy", "Indulge in the creamy and buttery flavor of Sargento Natural Sliced Havarti Cheese. This 7 oz package contains 10 slices, perfect for enhancing your favorite sandwiches, burgers, or snacks. Made from natural cheese off the block, Sargento ensures you get the highest quality with each slice. The Fresh-Lock feature keeps your cheese fresher longer, making it a convenient and delicious addition to your fridge.", "images/havarti.png"),
("Organic Half and Half", "Horizon", 500, 4.99, 2.1, False, "Dairy", "Enjoy the rich and creamy taste of Horizon Organic Half and Half in your coffee, tea, or favorite recipes. Made with non-GMO ingredients and certified USDA Organic, this half and half offers a natural and wholesome option for your daily routine. Packaged in a 1-quart (946 mL) carton, it's ultra-pasteurized for extended freshness. Elevate your beverages and dishes with the quality you trust from Horizon.", "images/half-half.png"),
("Organic 0% Fat Free Milk", "Horizon", 500, 3.99, 4.0, False, "Dairy", "Stay refreshed and healthy with Horizon Organic 0% Fat Free Milk. This half-gallon (1.89 L) carton provides high vitamin D to support bone health and is enriched with vitamins A & D. The ultra-pasteurized milk has a creamy texture without the fat, making it a perfect choice for those seeking a balanced diet. Certified USDA Organic, this milk is sourced from cows raised with no antibiotics, added hormones, or GMOs.", "images/fatfreemilk.png"),
("Brand Low Fat Cottage Cheese", "Daisy", 500, 3.99, 1.5, False, "Dairy", "Enjoy the wholesome goodness of Daisy Brand Low Fat Cottage Cheese. This 24 oz container of low fat, small curd cottage cheese is made with 2% milkfat and packed with 13g of protein per serving. Creamy and delicious, it's perfect for snacking, adding to your favorite recipes, or enjoying on its own. With no artificial additives, it's a pure and natural choice for health-conscious individuals.", "images/cottagecheese.png"),
("Cinnamon Roll Zero Sugar Coffee Creamer", "Nestlé", 500, 3.99, 2.0, False, "Dairy", "Indulge in the rich and delightful taste of cinnamon rolls with Nestlé Coffee mate Cinnamon Roll Zero Sugar Coffee Creamer. This 32 fl oz bottle offers a creamy, zero-sugar option that's triple churned and twice as rich as milk. Perfect for enhancing your coffee with a touch of cinnamon sweetness, it provides only 15 calories per tablespoon. Enjoy this recyclable bottle as an effortless way to elevate your daily coffee experience.", "images/coffesweatener.png"),
("Ultra Thin Sharp Cheddar Cheese", "Sargento", 500, 4.29, 0.43, False, "Dairy", "Enhance your meals with the rich, bold flavor of Sargento Ultra Thin Sharp Cheddar Cheese. This 6.84 oz package contains 18 ultra thin slices, perfect for sandwiches, burgers, and snacks. Made from natural cheese off the block, these slices are 45 calories each, offering a delightful and convenient way to add a touch of sharpness to your favorite dishes. The Fresh-Lock feature ensures your cheese stays fresh, making it a must-have in any kitchen.", "images/cheddar.png"),
("Premium Pure Cane Light Brown Sugar", "C&H", 500, 2.99, 2.0, False, "Ingredients", "Elevate your baking with C&H Premium Pure Cane Light Brown Sugar. This 32 oz (2 lb) package features a resealable zipper for convenience and freshness. Perfect for cookies, cakes, and other sweet treats, this non-GMO verified sugar adds a rich, molasses-like flavor to your recipes. Trusted since 1906, C&H brings you the quality and consistency you need for your baking happiness.", "images/brownsugar.png"),
("Italian Seasoning", "Simply Organic", 500, 4.99, 0.3, False, "Ingredients", "Add a burst of authentic Italian flavor to your dishes with Simply Organic Italian Seasoning. This 0.95 oz glass jar contains a blend of high-quality, USDA Certified Organic herbs, including oregano, marjoram, thyme, basil, rosemary, and sage. Perfect for enhancing pasta, sauces, meats, and vegetables, this seasoning mix brings the taste of Italy to your kitchen. The resealable jar ensures freshness, while the blend's robust flavor elevates any meal.", "images/basil.png"),
("Organic Bay Leaves", "Simply Organic", 500, 5.49, 0.15, False, "Ingredients", "Enhance your culinary creations with the aromatic flavor of Organic Bay Leaves. This 0.25 oz package contains whole, dried bay leaves, which are essential for soups, stews, sauces, and marinades. Sourced from organically grown bay trees, these leaves add a subtle, earthy taste and a fragrant aroma to your dishes. Perfect for slow-cooked recipes, the leaves can be removed before serving for a refined and delicious meal.", "images/bayleaf.png"),
("Butter Salted Sticks", "Great Value", 500, 4.29, 0.5, False, "Dairy", "Enhance your cooking and baking with Great Value Butter Salted Sticks. This 8 oz (227g) package contains two sticks of USDA Grade AA butter, ensuring top quality and rich flavor for all your culinary creations. Perfect for spreading, melting, or baking, this butter adds a touch of creamy goodness to any dish. Keep refrigerated for optimal freshness.", "images/Butter.png"),
("Chili Powder", "McCormick", 500, 3.99, 0.16, False, "Ingredients", "Elevate your dishes with the robust flavor of McCormick Chili Powder. This 2.5 oz (70 g) bottle delivers the trusted taste of McCormick, perfect for adding a kick to your chili, tacos, and other recipes. Non-GMO and made with quality ingredients, this chili powder ensures a bold and rich flavor in every sprinkle. The convenient bottle with a red cap keeps your spice fresh and ready to use.", "images/chilipowder.png"),
("1% Lowfat Chocolate Milk", "Great Value", 500, 3.99, 8.5, False, "Dairy", "Enjoy the rich and creamy taste of Great Value 1% Lowfat Chocolate Milk. This 1-gallon (3.78L) jug is packed with essential nutrients, including vitamins A and D, calcium, and potassium. Made with lowfat milk, cocoa, and a hint of sweetness, it's a delightful and nutritious treat for any time of day. Whether enjoyed chilled on its own or used in recipes, this chocolate milk is sure to please. Keep refrigerated for freshness.", "images/chocolatemilk.png"),
("Ground Cinnamon", "Great Value", 500, 2.29, 0.16, False, "Ingredients", "Add a warm and aromatic flavor to your recipes with Great Value Ground Cinnamon. This 2.5 oz (70g) container is perfect for baking, cooking, and adding a delicious touch to your beverages. Sourced from high-quality cinnamon, it offers a rich and authentic taste. The convenient resealable container ensures freshness, making it a staple in your spice cabinet.", "images/groundcinnamon.png"),
("Ground Ginger", "McCormick", 500, 4.99, 0.15, False, "Ingredients", "Add a warm and zesty kick to your recipes with McCormick Ground Ginger. This 0.7 oz (19g) container of ground ginger is perfect for baking, cooking, and adding a delightful flavor to your beverages. Sourced from premium quality ginger, it offers a vibrant and fresh taste. The convenient resealable container ensures lasting freshness, making it a staple in your spice collection.", "images/ginger.png"),
("Organic Garlic Powder", "McCormick", 500, 7.49, 1.04, False, "Ingredients", "Enhance the flavor of your dishes with McCormick Organic Garlic Powder. This 16.75 oz (474g) container offers a convenient way to add the rich taste of garlic to your cooking. Non-GMO and USDA Certified Organic, this powder ensures high quality and freshness. Perfect for seasoning meats, vegetables, soups, and more, it brings a robust and aromatic touch to your culinary creations.", "images/garlicpowder.png"),
("Lemon Pepper Seasoning", "Badia", 500, 6.49, 1.5, False, "Ingredients", "Add a zesty kick to your meals with Badia Lemon Pepper Seasoning. This 24 oz (1.5 lb or 680.4 g) container offers a flavorful blend of lemon and pepper, perfect for enhancing chicken, fish, and vegetables. Gluten-free and kosher, this seasoning mix brings a burst of freshness and a tangy twist to your favorite dishes. The convenient container with a yellow cap keeps your seasoning fresh and ready to use.", "images/lemonpepper.png"),
("Extra Virgin Olive Oil", "Pompeian", 500, 10.99, 4.25, False, "Ingredients", "Experience the robust and rich flavor of Pompeian Extra Virgin Olive Oil. This first cold pressed olive oil is perfect for salads, marinades, and cooking. The 68 fl oz (2 L) bottle ensures you have enough for all your culinary needs. Farmer owned since 1906, Pompeian guarantees quality and freshness in every bottle, making it a staple in your kitchen.", "images/oliveoil.png"),
("Paprika", "McCormick", 500, 3.99, 0.13, False, "Ingredients", "Enhance your dishes with the rich, vibrant flavor of McCormick Paprika. This 2.12 oz (60g) container of paprika delivers a mild, sweet taste and a vibrant red color, perfect for adding depth to your recipes. Made from high-quality peppers, McCormick Paprika is a versatile spice that can be used in a variety of dishes, from meats to vegetables to soups. The convenient container keeps your spice fresh and ready to use.", "images/paprika.png"),
("Grinder Black Peppercorns", "Morton", 500, 4.49, 1.24, False, "Ingredients", "Enhance your culinary creations with the robust flavor of Morton Grinder Black Peppercorns. This 1.24 oz (35g) grinder allows you to freshly grind pepper for an intense, aromatic experience. Trusted since 1848, Morton guarantees quality and consistency in every product. Perfect for seasoning meats, vegetables, and more, this black pepper adds a burst of flavor to any dish.", "images/pepper.png"),
("Salt", "Morton", 500, 1.99, 1.625, False, "Ingredients", "Trusted since 1848, Morton Salt is a staple in kitchens across the country. This 26 oz (737g) container of salt is perfect for all your cooking and baking needs. While it does not supply iodide, Morton Salt provides consistent quality and flavor that enhances the taste of your dishes. The container is easy to store and pour, making it a convenient addition to your pantry.", "images/salt.png"),
("Granulated Sugar", "Hill Country Fare", 500, 1.99, 2.0, False, "Ingredients", "Enhance your baking and cooking with Hill Country Fare Granulated Sugar. This 4 lb (1.81 kg) package of pure, refined sugar is perfect for all your sweet creations. Whether you're baking cookies, cakes, or sweetening beverages, this granulated sugar delivers consistent quality and taste. The simple, straightforward packaging makes it easy to identify, with both English and Spanish text for convenience.", "images/sugar.png"),
("Thyme Leaves", "McCormick", 500, 2.99, 0.37, False, "Ingredients", "Add a subtle minty flavor to your dishes with McCormick Thyme Leaves. This 0.37 oz (10.5 g) container features carefully selected, non-GMO thyme leaves that are perfect for enhancing the taste of soups, stews, sauces, and roasted meats. The clear container with a red lid ensures freshness and allows you to see the quality of the thyme leaves inside. A must-have for any kitchen, McCormick Thyme Leaves bring a touch of elegance to your culinary creations.", "images/thyme.png")
]



cursor.executemany("INSERT INTO product (name, brand, stock, price, weight, featured, category, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", test_products)
mydb.commit()
#formatting for the order items, name, brand, stock, price, weight ,featured, category, description, image#
#make sure data is consistent 


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
