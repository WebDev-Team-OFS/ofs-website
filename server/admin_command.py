#file where all the admin commands go
from flask import Blueprint, request, jsonify, session
from db_module import get_db_connection
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

admin_cmd_bp = Blueprint('admin_command', __name__)


#view all stock
@admin_cmd_bp.route('/admin/products', methods=['GET'])
@jwt_required()
def review_stock():
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403

        #admin_id = session['admin_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return jsonify(products), 200



    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Update Stock
@admin_cmd_bp.route('/admin/products/<int:product_id>/stock', methods=['PUT'])
@jwt_required()
def change_stock(product_id):
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403


        #admin_id = session['admin_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        data = request.get_json()   
        new_stock = data.get('stock')

        if new_stock is None or new_stock < 0:
            return jsonify({"error": "Invalid stock value"}), 400

        cursor.execute("UPDATE product SET stock = %s WHERE product_id = %s", (new_stock, product_id))
        db_connection.commit()

        return jsonify({"message": "Stock updated successfully"}), 200
    
    except Exception as e: 
        if db_connection:
            db_connection.rollback()
        return jsonify({"error": "An error occurred while updating stock", "details": str(e)}), 500

    finally:
        if cursor: 
            cursor.close
        if db_connection:
            db_connection.close()



# Update price
@admin_cmd_bp.route('/admin/products/<int:product_id>/price', methods=['PUT'])
@jwt_required()
def update_price(product_id):
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403

        #admin_id = session['admin_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        data = request.get_json()

        new_price = data.get('price')

        if new_price is None or new_price < 0:
            return jsonify({"error": "Invalid price value"}), 400

        cursor.execute("UPDATE product SET price = %s WHERE product_id = %s", (new_price, product_id))
        db_connection.commit()

        return jsonify({"message": "Price updated successfully"}), 200
    
    except Exception as e: 
        if db_connection:
            db_connection.rollback()
        return jsonify({"error": "An error occurred while updating price", "details": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()


#remove item
@admin_cmd_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_item(product_id):
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403

        #admin_id = session['admin_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        db_connection.commit()

        return jsonify({"message": "Product removed successfully"}), 200
    
    except Exception as e: 
        return jsonify({"error": "An error occurred while removing the product", "details": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()



#add item (this needs a fix due to still using session id)
@admin_cmd_bp.route('/admin/add_products', methods=['POST'])
@jwt_required()
def add_product():
    cursor = None
    db_connection = None
    try:
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403

        data = request.get_json()
        required_fields = ['name', 'brand', 'stock', 'price', 'weight', 'category', 'description']


        for field in required_fields:
                    if field not in data:
                        return jsonify({"error": f"Missing required field: {field}"}), 400
        
        image = data.get('image')

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("INSERT INTO product(name, brand, stock, price, weight, category, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['name'], data['brand'], data['stock'], data['price'], data['weight'], data['category'], data['description'], image))
        
        db_connection.commit()

        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        if db_connection:
            db_connection.rollback()
        return jsonify({"error": "An error occurred while adding the product", "details": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()



#add admin
@admin_cmd_bp.route("/add_admin", methods = ["POST"])
@jwt_required()
def add_admin():
    try:

        claims  = get_jwt()
        if not claims.get('is_admin', False):  
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")

        if not all([username, password, first_name, last_name, email]):
            return jsonify({"error": "All fields are required"}), 400
        
        hashed_password = generate_password_hash(password)

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        query = """
            INSERT INTO admin_info (username, password, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s)
            """
        
        cursor.execute(query, (username, hashed_password, first_name, last_name, email))
        db_connection.commit()

        return jsonify({"message": "Admin added successfully"}), 201
        
        

    except Exception as e: 
        return jsonify({"error": "An error occurred while adding the admin", "details": str(e)}), 500
    
    finally: 
        if cursor: 
            cursor.close()
        if db_connection:
            db_connection.close()
    


#remove admin
@admin_cmd_bp.route("/remove_admin", methods=["DELETE"])
@jwt_required()
def remove_admin():
    try:
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        
        data = request.get_json()
        #can be changed to user_id or something later
        username = data.get("username")

        if not username:
            return jsonify({"error": "Username is required"}), 400

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        # Check if the admin exists
        check_query = "SELECT * FROM admin_info WHERE username = %s"
        cursor.execute(check_query, (username,))
        admin = cursor.fetchone()

        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        # Delete the admin
        delete_query = "DELETE FROM admin_info WHERE username = %s"
        cursor.execute(delete_query, (username,))
        db_connection.commit()

        return jsonify({"message": f"Admin '{username}' removed successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while removing the admin", "details": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()



#more admin commands
#add view all admins or something