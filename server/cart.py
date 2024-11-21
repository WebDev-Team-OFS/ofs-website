from flask import Blueprint, jsonify, session, request
from db_module import get_db_connection



cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/api/view_cart', methods=['GET'])
def view_cart():
    """View the current user's cart."""
    if 'user_id' not in session:
        return jsonify({"error": "User is not logged in"}), 401

    user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
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
        cursor.close()
        db_connection.close()

    

@cart_bp.route('/api/add_to_cart/', methods=['POST'])
def add_to_cart():
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
        cursor.close()
        db_connection.close()


@cart_bp.route('/api/remove_from_cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return jsonify({"error": "User is not logged in"}), 401

    user_id = session['user_id']
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            DELETE FROM user_cart
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        db_connection.commit()

        return jsonify({"message": "Item removed from cart"}), 200
    except Exception as e:
        return jsonify({"error":  "Item not in cart"}), 404
    finally:
        cursor.close()
        db_connection.close()



@cart_bp.route('/api/update_cart_item', methods=['PUT'])
def update_cart_item():
    """Update the quantity of an item in the cart."""
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized, please log in first"}), 401

    user_id = session['user_id']
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
        cursor.close()
        db_connection.close()


#we should add a api to commit the order information to db 

@cart_bp.route('/api/checkout', methods = ['POST'])
def checkout():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "User is not logged in"}), 401
    
        user_id = session['user_id']
        data = request.get_json()
        items = data.get('items')

        if not items or not isinstance(items, list):
            return jsonify({"error": "No items provided or invalid format"}), 400
    
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        for item in items:
            product_id = item.get('product_id')
            amount = item.get('quantity')
            cost = item.get('price')

            if not all([product_id, amount, cost]):
                return jsonify({"error": "Not all parameters present"}), 401
            

            cursor.execute("""
                INSERT INTO orders (user_id, product_id, amount, cost)
                VALUES (%s, %s, %s, %s)
                """, (user_id, product_id, amount, cost))
        
        db_connection.commit

        cursor.close()
        db_connection.close()

        return jsonify({"Order Success": "All orders are put into the table"}), 201

    except Exception as e:
        # Rollback in case of an error
        if get_db_connection:
            get_db_connection.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        # Ensure resources are closed
        if cursor:
            cursor.close()
        if get_db_connection:
            get_db_connection.close()


