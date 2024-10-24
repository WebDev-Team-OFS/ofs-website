from flask import Blueprint, jsonify, request
from db_module import get_db_connection
# Change app route as needed
auth_bp = Blueprint('auth', __name__)

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
        cursor.execute("SELECT user_id, username, first_name, last_name, email, is_admin FROM user_info WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        # Close connection
        cursor.close()
        db_connection.close()

        if user:
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500