#user queries go here such as search item
from flask import Blueprint, jsonify, request, session, current_app
from db_module import get_db_connection
from datetime import timedelta


user_cmd_bp = Blueprint('user_command', __name__)



#make sure you use the protected before accesses these


@user_cmd_bp.route("/api/profile", methods = ['GET'])
def view_profile():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorazied access, login first"}), 401
        
        user_id = session['user_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("""
                Select user_id, username, first_name, last_name, email data_create, from user_info where user_id = %s  
                    
                    """, (user_id))
        user_profile = cursor.fetchone()


        cursor.close()
        db_connection.close()

        if user_profile:
            return jsonify({"profile": user_profile}), 200
        else:
            return jsonify({"error": "profile not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()


@user_cmd_bp.route("/api/profile", methods = ['PUT'])
def edit_profile():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthoraized, login first"}), 401
        
        user_id = session['user_id']
        data = request.get_json()

        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')


        if not all([username, first_name, last_name, email]):
            return jsonify({"error": "All fields must be filled"}), 400
        
        db_connection = get_db_connection()
        cursor = db_connection.cursor()


        cursor.execute("""
            UPDATE user_info
            SET username = %s, first_name= %s, last_name =%s, email = %s  
            Where user_id = %s
        """, (username, first_name, last_name, email, user_id))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({"message": "user profile updated"}), 200
    except Exception as e:
        if db_connection:
            db_connection.rollback()
        return  jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
        




#add past transactions
