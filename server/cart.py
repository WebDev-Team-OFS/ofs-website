from flask import Blueprint, jsonify, session, request
from db_module import get_db_connection


cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/api/view_cart', methods=['GET'])
def view_cart():
    cart = session.get("cart", {})
    return jsonify({"cart": cart})

@cart_bp.route('/api/add_to_cart/<int:product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(product_id, quantity):
    cart = session.get("cart", {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    session["cart"] = cart
    return jsonify({"message": "Item added to cart"})

@cart_bp.route('/api/remove_from_cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if product_id in cart:
        del cart[product_id]
        session["cart"] = cart
        return jsonify({"message": "Item removed from cart"})
    return jsonify({"error": "Item not in cart"}), 404

@cart_bp.route('/api/update_cart_item/<int:product_id>/<int:new_quantity>', methods=['PUT'])
def update_cart_item(product_id, new_quantity):
    cart = session.get("cart", {})
    if product_id in cart:
        if new_quantity > 0:
            cart[product_id] = new_quantity
        else:
            del cart[product_id]  # Remove item if quantity is 0
        session["cart"] = cart
        return jsonify({"message": "Cart updated"})
    return jsonify({"error": "Item not in cart"}), 404



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


