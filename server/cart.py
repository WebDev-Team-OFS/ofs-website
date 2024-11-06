from flask import Flask,jsonify
from db_module import get_db_connection


app = Flask(__name__)
#create cart for user 

#the functions are not connected to the server 10/31/2024 Bryan 
#view cart
@app.route('/view_cart/<int:user_id>', methods= ['GET'])
def view_cart(user_id):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("""
        SELECT name, p.price, c.quantity, (p.price * c.quantity) AS total
        FROM cart
        JOIN product p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    
    items = cursor.fetchall()
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({"message": "Item removed from cart"})


#remove item from cart 
@app.route('/remove_from_cart/<int:user_id>/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("""
        DELETE FROM cart WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({"message": "Item removed from cart"})

#increase or decrease items in cart 

@app.route('/update_cart_item/<int:user_id>/<int:product_id>/<int:new_quantity>', methods =['PUT'])
def update_cart_item(user_id, product_id, new_quantity):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    if new_quantity > 0:
        cursor.execute("""
            UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s
        """, (new_quantity, user_id, product_id))
    else:
        # Remove item if quantity is 0
        cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s",(user_id, product_id))
        
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({"message": "Cart updated"})



if __name__ == "__main__":
    app.run(debug=True)
