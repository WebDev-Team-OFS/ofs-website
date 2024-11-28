from flask import Blueprint, jsonify, session, request
from db_module import get_db_connection
import json


cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/api/view_cart', methods=['GET'])
def view_cart():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "User is not logged in"}), 401

    user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # View the current user's cart
        cursor.execute("""
            SELECT product_id, quantity
            FROM user_cart
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

    

@cart_bp.route('/api/add_to_cart/', methods=['POST'])
def add_to_cart():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "User is not logged in"}), 401

    user_id = session['user_id']
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
            FROM user_cart
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Update quantity if item already exists
            new_quantity = existing_item['quantity'] + quantity
            cursor.execute("""
                UPDATE user_cart
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
            """, (new_quantity, user_id, product_id))
        else:
            # Add new item to the cart
            cursor.execute("""
                INSERT INTO user_cart (user_id, product_id, quantity)
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


@cart_bp.route('/api/remove_from_cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "User is not logged in"}), 401

    user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Verify item is in cart and remove from cart 
        cursor.execute("""
            DELETE FROM user_cart
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




@cart_bp.route('/api/update_cart_item', methods=['PUT'])
def update_cart_item():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized, please log in first"}), 401

    user_id = session['user_id']
    data = request.get_json()
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')
    
    # Verify that product id and quantity values are provided
    if not all([product_id, new_quantity]):
        return jsonify({"error": "Product ID and new quantity are required"}), 400

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Update the quantity of an item in the cart
        if new_quantity > 0:
            # Update the quantity
            cursor.execute("""
                UPDATE user_cart
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
            """, (new_quantity, user_id, product_id))
        else:
            # Remove the item if the quantity is 0
            cursor.execute("""
                DELETE FROM user_cart
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
def checkout():
    cursor = None
    db_connection = None
    try:
        if 'user_id' not in session:
            return jsonify({"error": "User is not logged in"}), 401
            
        user_id = session['user_id']
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        
        # Start transaction
        db_connection.begin()
        
        # Get cart items
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.stock_quantity 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            return jsonify({"error": "Cart is empty. Please add items before checking out."}), 400
        
        total_price = 0

        # Check inventory and calculate total price
        for item in cart_items:
            product_id = item['product_id']
            cart_qty = item['quantity']
            stock_qty = item['stock_quantity']
            price = item['price']

            if stock_qty < cart_qty:
                db_connection.rollback()
                return jsonify({"error": f"Not enough stock for product ID {product_id}"}), 400

            total_price += cart_qty * price
            
        # Check inventory and update stocks
        for product_id, cart_qty, stock_qty in cart_items:
            if stock_qty < cart_qty:
                db_connection.rollback()
                return jsonify({
                    "error": f"Not enough stock for product {product_id}"
                }), 400
                
            # Update product inventory
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
            """, (cart_qty, product_id))
        
        # Create order record
        cursor.execute("""
            INSERT INTO orders (user_id, status, created_at)
            VALUES (%s, 'pending', NOW())
        """, (user_id,))
        order_id = cursor.lastrowid
        
        # Move cart items to order_items
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity)
            SELECT %s, product_id, quantity 
            FROM cart WHERE user_id = %s
        """, (order_id, user_id))
        
        # Clear user's cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        # Commit transaction
        db_connection.commit()
        
        return jsonify({
            "message": "Checkout successful",
            "order_id": order_id,
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
