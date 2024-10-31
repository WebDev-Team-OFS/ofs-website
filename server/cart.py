from flask import Flask,jsonify

from db_module import get_db_connection
#create cart for user 


# #add product to cart


# def add_to_cart(user_id, product_id, quantity):
#     cursor.execute("""
#         SELECT * FROM cart WHERE user_id = %s AND product_id = %s
#     """, (user_id, product_id))
    
#     cart_item = cursor.fetchone()
    
#     if cart_item:
#         cursor.execute("""
#             UPDATE cart SET quantity = quantity + %s WHERE user_id = %s AND product_id = %s
#         """, (quantity, user_id, product_id))
#     else:
#         cursor.execute("""
#             INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)
#         """, (user_id, product_id, quantity))
    
#     mydb.commit()

#view cart
def view_cart(user_id):
    cursor.execute("""
        SELECT p.name, p.price, c.quantity, (p.price * c.quantity) AS total
        FROM cart c
        JOIN product p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    
    for item in cursor.fetchall():
        print(item)


#remove item from cart 

def remove_from_cart(user_id, product_id):
    cursor.execute("""
        DELETE FROM cart WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))
    mydb.commit()

#increase or decrease items in cart 


def update_cart_item(user_id, product_id, new_quantity):
    if new_quantity > 0:
        cursor.execute("""
            UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s
        """, (new_quantity, user_id, product_id))
    else:
        remove_from_cart(user_id, product_id)  # Remove item if quantity is 0
    mydb.commit()


