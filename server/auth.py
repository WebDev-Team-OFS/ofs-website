from flask import Blueprint, jsonify, request, session
from db_module import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
# Change app route as needed
auth_bp = Blueprint('auth', __name__)




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
        cursor.execute("SELECT user_id, username, first_name, last_name, email, is_admin FROM user_info WHERE email = %s", (email))
        user = cursor.fetchone()

        # Close connection
        cursor.close()
        db_connection.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            user.pop('password')
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#registration api end point
@auth_bp.route("/api/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_passowrd = data.get('confirm_password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        is_admin = data.get('is_admin', False)

        if not all([username, password, first_name, last_name, email]):
            return jsonify({"error": "All fields are required"}), 400
        if password != confirm_passowrd:
            return jsonify ({"error": "Passwords do not match"}), 400
        
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("Select email from user_info WHERE email = %s",(email))

        if cursor.fetchone():
            cursor.close()
            db_connection.close()
            return jsonify({"error": "Email already registered"}),400
        
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO user_info (username, password, first_name, last_name, email, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, first_name, last_name, email, is_admin))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@auth_bp.route("/api/protected", methods=["GET"])
def protected():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized, please login first"}), 401

    # Get user data from session
    user_id = session['user_id']
    username = session['username']
    return jsonify({"message": f"Welcome {username}!", "user_id": user_id}), 200

@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()  # Clears the session data
    return jsonify({"message": "Logged out successfully"}), 200






