#file where all the admin commands go
from flask import Blueprint, request, jsonify
from db_module import get_db_connection
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import os
import json

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
# @admin_cmd_bp.route('/admin/products/<int:product_id>/stock', methods=['POST'])
# @jwt_required()
# def change_stock(product_id):
#     try: 
#         claims = get_jwt()
#         if not claims.get('is_admin', False):
#             return jsonify({"error": "Unauthorized access, admin only"}), 403


#         #admin_id = session['admin_id']

#         db_connection = get_db_connection()
#         cursor = db_connection.cursor(dictionary=True)
#         data = request.get_json()   
#         new_stock = data.get('stock')

#         if new_stock is None or new_stock < 0:
#             return jsonify({"error": "Invalid stock value"}), 400

#         cursor.execute("UPDATE product SET stock = %s WHERE product_id = %s", (new_stock, product_id))
#         db_connection.commit()

#         return jsonify({"message": "Stock updated successfully"}), 200
    
#     except Exception as e: 
#         if db_connection:
#             db_connection.rollback()
#         return jsonify({"error": "An error occurred while updating stock", "details": str(e)}), 500

#     finally:
#         if cursor: 
#             cursor.close
#         if db_connection:
#             db_connection.close()

@admin_cmd_bp.route('/api/admin/update-product/', methods=['PUT'])
@jwt_required()
def update_product():
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403


        #admin_id = session['admin_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        data = request.get_json()   
        new_brand = data.get('brand')
        new_name = data.get('name')
        new_category = data.get('category')
        new_price = data.get('price')
        new_weight = data.get('weight')
        new_stock = data.get('stock')
        new_featured = data.get('featured')
        new_description = data.get('description')
        product_id = data.get('product_id')

        # if new_stock is None or new_stock < 0:
        #     return jsonify({"error": "Invalid stock value"}), 400

        cursor.execute("UPDATE product SET brand = %s, name = %s, category = %s, price = %s, weight = %s, stock = %s, featured = %s, description = %s WHERE product_id = %s", (new_brand, new_name, new_category, new_price, new_weight, new_stock, new_featured, new_description, product_id))
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

@admin_cmd_bp.route('/api/admin/add-product/', methods=['POST'])
@jwt_required()
def add_product():
    cursor = None;
    db_connection = None;
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403



        temp_data = request.form.get('data')
        image = request.files['image']


        data = None;
        if temp_data:
            data = json.loads(temp_data)  # Parse JSON string into a dictionary
        new_brand = data.get('brand')
        new_name = data.get('name')
        new_category = data.get('category')
        new_price = data.get('price')
        new_weight = data.get('weight')
        new_stock = data.get('stock')
        new_featured = data.get('featured')
        new_description = data.get('description')

        #path to upload folder for image
        upload_folder = os.path.join(os.getcwd(),'images')

        if image.filename == '' or not image:
            return jsonify({"error": "No selected file"}), 400
        
        #sanitozes file name i think 
        image_filename = secure_filename(image.filename)

        #image path used to upload to mySQL DB
        relative_image_path = os.path.join('images', image_filename)

        if image:
            #saves image to uplad folder 
            image_path = os.path.join(upload_folder, image_filename)
            image.save(image_path)


        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("""INSERT INTO product (brand, name, category, price, weight, stock, featured, description, image) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s)""", (new_brand, new_name, new_category, new_price, new_weight, new_stock, new_featured, new_description, relative_image_path))
        db_connection.commit()

        return jsonify({"message": "Product added successfully"}), 200
    
    except Exception as e: 
        if db_connection:
            db_connection.rollback()
        return jsonify({"error": "An error occurred while adding the product", "details": str(e)}), 500

    finally:
        if cursor: 
            cursor.close
        if db_connection:
            db_connection.close()

@admin_cmd_bp.route('/api/admin/update-image/', methods=['PUT'])
@jwt_required()
def update_image():
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        image = request.files['image']
        product_id = request.form.get('product_id')

        #path to upload folder
        upload_folder = os.path.join(os.getcwd(),'images')

        if image.filename == '' or not image:
            return jsonify({"error": "No selected file"}), 400
        
        #sanitozes file name i think 
        image_filename = secure_filename(image.filename)

        #image path used to upload to mySQL DB
        relative_image_path = os.path.join('images', image_filename)

        if image:
            #saves image to uplad folder 
            image_path = os.path.join(upload_folder, image_filename)
            image.save(image_path)

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("UPDATE product SET image = %s WHERE product_id = %s", (relative_image_path, product_id))
        db_connection.commit()

        return jsonify({"message": "File uploaded successfully", "path": image_path}), 200
    except Exception as e: 
        return jsonify({"error": "An error occurred while uploading image", "details": str(e)}), 500
   




# NOT NEEDED?
# Update price
# @admin_cmd_bp.route('/admin/products/<int:product_id>/price', methods=['PUT'])
# @jwt_required()
# def update_price(product_id):
#     try: 
#         claims = get_jwt()
#         if not claims.get('is_admin', False):
#             return jsonify({"error": "Unauthorized access, admin only"}), 403

#         #admin_id = session['admin_id']

#         db_connection = get_db_connection()
#         cursor = db_connection.cursor(dictionary=True)
#         data = request.get_json()

#         new_price = data.get('price')

#         if new_price is None or new_price < 0:
#             return jsonify({"error": "Invalid price value"}), 400

#         cursor.execute("UPDATE product SET price = %s WHERE product_id = %s", (new_price, product_id))
#         db_connection.commit()

#         return jsonify({"message": "Price updated successfully"}), 200
#     except Exception as e: 
#         if db_connection:
#             db_connection.rollback()
#         return jsonify({"error": "An error occurred while updating price", "details": str(e)}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if db_connection:
#             db_connection.close()


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


#OLD ADD PRODUCT API
# #add item (this needs a fix due to still using session id)
# @admin_cmd_bp.route('/admin/add_products', methods=['POST'])
# @jwt_required()
# def add_product_test():
#     cursor = None
#     db_connection = None
#     try:
#         claims = get_jwt()
#         if not claims.get('is_admin', False):
#             return jsonify({"error": "Unauthorized access, admin only"}), 403

#         data = request.get_json()
#         required_fields = ['name', 'brand', 'stock', 'price', 'weight', 'category', 'description']


#         for field in required_fields:
#                     if field not in data:
#                         return jsonify({"error": f"Missing required field: {field}"}), 400
        
#         image = data.get('image')

#         db_connection = get_db_connection()
#         cursor = db_connection.cursor(dictionary=True)

#         cursor.execute("INSERT INTO product(name, brand, stock, price, weight, category, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#                 (data['name'], data['brand'], data['stock'], data['price'], data['weight'], data['category'], data['description'], image))
        
#         db_connection.commit()

#         return jsonify({"message": "Product added successfully"}), 201
#     except Exception as e:
#         if db_connection:
#             db_connection.rollback()
#         return jsonify({"error": "An error occurred while adding the product", "details": str(e)}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if db_connection:
#             db_connection.close()



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