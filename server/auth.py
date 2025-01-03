from flask import Blueprint, jsonify, request
from db_module import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

# Change app route as needed
auth_bp = Blueprint('auth', __name__)





@auth_bp.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get('is_admin', False):
            access_token = create_access_token(identity=current_user, 
                                               additional_claims={"is_admin": True},
                                               expires_delta=timedelta(minutes=5))
        else:
            access_token = create_access_token(identity=current_user)

        return jsonify({
            "access_token": access_token,
            "message": "Token refreshed"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#login in api end point
@auth_bp.route("/api/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Get database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        # Query to check for user with provided email and password
        cursor.execute("SELECT user_id, username, first_name, last_name, email, password FROM user_info WHERE email = %s", (email,))
        user = cursor.fetchone()

        # Close connection
        cursor.close()
        db_connection.close()

        if user and check_password_hash(user['password'], password):
            user.pop('password')  # Remove password from response for security
            access_token = create_access_token(identity=str(user['user_id']),
                                                additional_claims={"is_admin": False})
            refresh_token = create_refresh_token(identity=str(user['user_id']))

            return jsonify({"message": "Login successful", "user": user, "access_token": access_token,
                "refresh_token": refresh_token
            }),200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#validate the user input
def validate_user_pass(data):
    """Validate admin input data"""
    errors = []
    
    required_fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if data.get('email') and '@' not in data['email'] or "." not in data['email']:
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
        if len(data['username']) > 50:
            errors.append("Username must be less than 50 characters")
            
    return errors


#registration api end point
@auth_bp.route("/api/register", methods=['POST'])
def register():
    cursor = None
    db_connection = None
    try:
        data = request.get_json()

        user_errors = validate_user_pass(data)
        if user_errors:
            return jsonify({"error": user_errors}), 400


        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        if not all([username, password, first_name, last_name, email]):
            return jsonify({"error": "All fields are required"}), 400
        if password != confirm_password:
            return jsonify ({"error": "Passwords do not match"}), 400
        
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("Select email from user_info WHERE email = %s",(email,))

        if cursor.fetchone():
            cursor.close()
            db_connection.close()
            return jsonify({"error": "Email already registered"}),400
        
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO user_info (username, password, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, hashed_password, first_name, last_name, email))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
    

#check if the person is allowed in
@auth_bp.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get('is_admin'):
            return jsonify({"error": "Access denied. Log into user account"}), 403
        return jsonify({
            "message": "Access granted",
            "current_user": current_user
        }),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#check if the person is allowed in
#security check ig (don't ask me)
@auth_bp.route("/api/admin/protected", methods=["GET"])
@jwt_required()
def admin_protected():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"error": "Access denied"}), 403

        return jsonify({"message": "Access granted", "current_user": current_user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#universal logout end point
@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    try:
        response = jsonify({"message": "Logged out successfully"})
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#login end point for admin
@auth_bp.route("/api/admin/login", methods = ['POST'])
def admin_login():
    cursor = None
    db_connection = None
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT emp_id, username, first_name, last_name, email, password FROM admin_info WHERE email = %s", (email,))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin['password'], password):
            admin.pop('password')
            admin['is_admin'] = True
            access_token = create_access_token(identity=str(admin['emp_id']), 
                                               expires_delta=timedelta(minutes=5), 
                                               additional_claims={"is_admin": True})
            refresh_token = create_refresh_token(identity=admin['emp_id'])

            return jsonify({"message": "Login successful", "admin": admin, "access_token": access_token, "refresh_token": refresh_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
