from flask import Blueprint, jsonify, session

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
