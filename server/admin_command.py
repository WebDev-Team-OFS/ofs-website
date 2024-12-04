#file where all the admin commands go
from flask import Blueprint, request, jsonify
from db_module import get_db_connection
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt
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

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return jsonify(products), 200



    except Exception as e:
        return jsonify({"error": str(e)}), 500



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


        cursor.close()
        db_connection.close()

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

        db_connection.close()
        cursor.close()

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



'''new change remove if broken'''
def validate_image(file):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    errors =[]
    if not file:
        errors.append("No file found")
        return errors
    filename = file.filename
    if '.' not in filename or filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        errors.append("Invalid file type")
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0) 

    if file_length > 2* 1024 *1024 *1024:
        errors.append("File too large")
    
    return errors


@admin_cmd_bp.route('/api/admin/update-image/', methods=['PUT'])
@jwt_required()
def update_image():
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        
        image = request.files['image']
        product_id = request.form.get('product_id')

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400
        
        errors = validate_image(image) #<-- new change
        if errors:
            return jsonify({"error": errors}), 400

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

        cursor.close()
        db_connection.close()

        return jsonify({"message": "File uploaded successfully", "path": image_path}), 200
    except Exception as e: 
        return jsonify({"error": "An error occurred while uploading image", "details": str(e)}), 500
   



#remove item
@admin_cmd_bp.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_item(product_id):
    try: 
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        db_connection.commit()


        cursor.close()  
        db_connection.close()
        return jsonify({"message": "Product removed successfully"}), 200
    
    except Exception as e: 
        return jsonify({"error": "An error occurred while removing the product", "details": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

'''new change remove if broken'''
def validate_admin_data(data):
    """Validate admin input data"""
    errors = []
    
    required_fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if data.get('email') and '@' not in data['email']:
        errors.append("Invalid email format")

    if data.get('password'):
        if len(data['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in data['password']):
            errors.append("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in data['password']):
            errors.append("Password must contain at least one number")

    if data.get('username'):
        if len(data['username']) < 3:
            errors.append("Username must be at least 3 characters")
        if not data['username'].isalnum():
            errors.append("Username must contain only letters and numbers")
            
    return errors



#add admin
@admin_cmd_bp.route("/api/admin/add_admin", methods = ["POST"])
@jwt_required()
def add_admin():
    try:
        claims  = get_jwt()
        if not claims.get('is_admin', False):  
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        
        
        data = request.get_json()
        admin_errors = validate_admin_data(data)  #<-- new change
        if admin_errors:
            return jsonify({"error": admin_errors}), 400

        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")

        if not all([username, password, first_name, last_name, email, confirm_password]):
            return jsonify({"error": "All fields are required"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400
        
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
@admin_cmd_bp.route("/api/admin/remove_admin/<int:emp_id>", methods=["DELETE"])
@jwt_required()
def remove_admin(emp_id):
    try:
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({"error": "Unauthorized access, admin only"}), 403
        


        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        # Check if the admin exists
        check_query = "SELECT * FROM admin_info WHERE emp_id = %s"
        cursor.execute(check_query, (emp_id,))
        admin = cursor.fetchone()

        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        # Delete the admin
        delete_query = "DELETE FROM admin_info WHERE emp_id = %s"
        cursor.execute(delete_query, (emp_id,))
        db_connection.commit()


        cursor.close()
        db_connection.close()
        return jsonify({"message": f"Admin '{emp_id}' removed successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while removing the admin", "details": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

@admin_cmd_bp.route("/api/admin/view_admins", methods=["GET"])
@jwt_required()
def view_admins():
    try:

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        # Check if the admin exists
        check_query = "SELECT emp_id, date_created, email, first_name, last_name, username FROM admin_info"
        cursor.execute(check_query)
        admins = cursor.fetchall()

        if not admins:
            return jsonify({"error": "Admin accounts not found"}), 404
        
        db_connection.commit()

        cursor.close()
        db_connection.close()


        return jsonify({"admins": admins}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while removing the admin", "details": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

#more admin commands
#add view all admins or something