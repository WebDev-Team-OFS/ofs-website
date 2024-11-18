from flask import Blueprint, jsonify, request, session, current_app, make_response
from db_module import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
# Change app route as needed
auth_bp = Blueprint('auth', __name__)





#might be really scuffed
@auth_bp.before_app_request
def set_admin_session_lifetime():
    """Sets a shorter session duration for admin accounts."""
    if 'admin_id' in session:
        session.permanent = True  # Enables the use of PERMANENT_SESSION_LIFETIME
        current_app.permanent_session_lifetime = timedelta(minutes=1)
    elif 'user_id' in session:
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=5)

    #legit don't know what is happening (maybe work since rip login page AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)

#the user time will update if they are doing something on the website
@auth_bp.before_app_request
def renew_session():
    #if 'user_id' in session or 'admin_id' in session:
    #    session.modified = True

    if ('user_id' in session or 'admin_id' in session) and request.endpoint not in ('static',):
        session.modified = True


@auth_bp.before_app_request
def validate_session():
    """Ensure the user is logged out if session data is invalid."""
    if 'user_id' not in session and 'admin_id' not in session:
        # Optionally: Clear client-side cookies if session is invalid
        if request.cookies.get('session'):
            response = make_response(jsonify({"error": "Session expired, please log in again."}))
            response.set_cookie('session', '', expires=0)
            return response




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
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            user.pop('password')
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()


#registration api end point
@auth_bp.route("/api/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
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
    


@auth_bp.route("/api/protected", methods=["GET"])
def protected():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized, please login first"}), 401

    # Get user data from session
    user_id = session['user_id']
    username = session['username']
    # session_expiry = session.permanent_session_lifetime.total_seconds() if session.permanent else None
    
    return jsonify({"message": f"Welcome {username}!", "user_id": user_id}), 200



#check if the person is allowed in
#security check ig (don't ask me)
@auth_bp.route("/api/admin/protected", methods=["GET"])
def admin_protected():
    if 'admin_id' not in session:
        return jsonify({"error": "Unauthorized, admin access only"}), 401
    return jsonify({"message": "Welcome, admin!"}), 200





@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()  # Clears the session data

    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie('session', '', expires=0)
    response.set_cookie('admin_id', '', expires=0)
    response.set_cookie('user_id', '', expires=0)

    return response, 200



@auth_bp.route("/api/admin/login", methods = ['POST'])
def admin_login():
    cursor = None;
    db_connection = None;
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
            session.clear()
            session['admin_id'] = admin['emp_id']
            session['admin_username'] = admin['username']
            admin.pop('password')  # Remove password from response for security
            return jsonify({"message": "Admin login successful", "admin": admin}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()



