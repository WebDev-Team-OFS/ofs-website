from flask import Blueprint, jsonify, session, request
from db_module import get_db_connection
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/api/view_cart', methods=['GET'])
@jwt_required()
def view_cart():
    """View the current user's cart."""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "User is not logged in"}), 401

    # user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT product_id, quantity
            FROM cart
            WHERE user_id = %s
        """, (user_id,))
        cart = cursor.fetchall()
        return jsonify({"cart": cart}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    
#adds item to the users temporary cart
@cart_bp.route('/api/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "User is not logged in"}), 401
    
    # user_id = session['user_id']
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not all([product_id, quantity]):
        return jsonify({"error": "Not all parameters present"}), 400

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Check if the product is already in the cart
        cursor.execute("""
            SELECT quantity
            FROM cart
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Update quantity if item already exists
            new_quantity = existing_item['quantity'] + quantity
            cursor.execute("""
                UPDATE cart
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
            """, (new_quantity, user_id, product_id))
        else:
            # Add new item to the cart
            cursor.execute("""
                INSERT INTO cart (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (user_id, product_id, quantity))

        db_connection.commit()
        return jsonify({"message": "Item added to cart"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

#removes item from the users temporary cart
@cart_bp.route('/api/remove_from_cart/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "User is not logged in"}), 401

    # user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            DELETE FROM cart
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        db_connection.commit()

        return jsonify({"message": "Item removed from cart"}), 200
    except Exception as e:
        return jsonify({"error":  "Item not in cart"}), 404
    finally:
        if cursor:  
            cursor.close()
        if db_connection:
            db_connection.close()



#if the users adds more items later to the cart
@cart_bp.route('/api/update_cart_item', methods=['PUT'])
@jwt_required()
def update_cart_item():
    print("STARTING>?")
    """Update the quantity of an item in the cart."""
    user_id = get_jwt_identity()
    if not user_id: 
        return jsonify({"error": "User is not logged in"}), 401 

    # user_id = session['user_id']
    data = request.get_json()
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')

    if not all([product_id, new_quantity]):
        return jsonify({"error": "Product ID and new quantity are required"}), 400

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        if new_quantity > 0:
            # Update the quantity
            cursor.execute("""
                UPDATE cart
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
            """, (new_quantity, user_id, product_id))
        else:
            # Remove the item if the quantity is 0
            cursor.execute("""
                DELETE FROM cart
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))

        db_connection.commit()
        return jsonify({"message": "Cart updated successfully"})
    except Exception as e:
        return jsonify({"error": "Item not in cart"}), 404
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()


#a new api to get all orders and to update the database with the status of the order
@cart_bp.route('/api/checkout', methods=['POST'])
@jwt_required()
def checkout():
    print("STARTING--------------------------------------------------------------")
    cursor = None
    db_connection = None
    try:
        user_id = get_jwt_identity()
        if not user_id: 
            return jsonify({"error": "User is not logged in"}), 401 
        print("EHH??")
            
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        print("HI!!")# tf is this
        
        # Start transaction
        db_connection.start_transaction() 
        print("ARE WE THERE YET?")
        
        # Get cart items
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.stock, p.price, p.weight
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        print("WE GOT THE CART")
        print(cart_items)
        
        if not cart_items:
            return jsonify({"error": "Cart is empty. Please add items before checking out."}), 400
        
        total_price = 0
        total_weight = 0;

        # Check inventory and calculate total price
        for item in cart_items:
            product_id = item['product_id']
            cart_qty = item['quantity']
            stock_qty = item['stock']
            price = item['price']
            weight = item['weight']

            if stock_qty < cart_qty:
                db_connection.rollback()
                return jsonify({"error": f"Not enough stock for product ID {product_id}"}), 400

            total_price += cart_qty * price
            total_weight += cart_qty * weight
        print("DID WE GET TOTAL PRICE?")


            
        # Check inventory and update stocks
        for item in cart_items:
            product_id = item['product_id']
            cart_qty = item['quantity']
            stock_qty = item['stock']
            price = item['price']
            if stock_qty < cart_qty:
                db_connection.rollback()
                return jsonify({
                    "error": f"Not enough stock for product {product_id}"
                }), 400
            print("almost?")
            # Update product inventory
            cursor.execute("""
                UPDATE product 
                SET stock = stock - %s
                WHERE product_id = %s
            """, (cart_qty, product_id))
        print("ALMOST!!")
        # Create order record
       
        for item in cart_items:
            item['price'] = float(item['price'])
            item['weight'] = float(item['weight'])

        print(cart_items)
        cart_json = json.dumps(cart_items)
        print("DID THIS WORK?")

        if total_weight > 20:
            total_price +=5


        cursor.execute("""
            INSERT INTO orders (user_id, total_price, total_weight, order_date, order_items)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (user_id, total_price, total_weight, json.dumps(cart_items)))
        print("LOL")
        
        # Move cart items to order_items
        # cursor.execute("""
        #     INSERT INTO order_items (order_id, product_id, quantity)
        #     SELECT %s, product_id, quantity 
        #     FROM cart WHERE user_id = %s
        # """, (order_id, user_id))
        
        # Clear user's cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        # Commit transaction
        db_connection.commit()
        
        return jsonify({
            "message": "Checkout successful",
            # "order_id": order_id,
            "total_price": total_price
        }), 200

    except Exception as e:
        if db_connection:
            db_connection.rollback()
        return jsonify({"error": f"Checkout failed: {str(e)}"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

