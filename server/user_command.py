#user queries go here such as search item
from flask import Blueprint, jsonify, request
from db_module import get_db_connection
from datetime import timedelta
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

user_cmd_bp = Blueprint('user_command', __name__)


#whole fine needs to change dependent on JWT or sessions

#make sure you use the protected before accesses these


@user_cmd_bp.route("/api/profile", methods = ['GET'])
@jwt_required() 
def view_profile():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized access, login first"}), 401
        
        # user_id = session['user_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        print("are we here")

        cursor.execute("""
                SELECT user_id, username, first_name, last_name, email, date_created
                    FROM user_info 
                    WHERE user_id = %s  
                """, (user_id,))
        user_profile = cursor.fetchone()
        print("here?")


        cursor.close()
        db_connection.close()

        if user_profile:
            return jsonify({"profile": user_profile}), 200
        else:
            return jsonify({"error": "profile not found"}), 404
    
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

#unused api point
@user_cmd_bp.route("/api/profile", methods = ['PUT'])
@jwt_required()
def edit_profile():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized access, login first"}), 401
        
        # user_id = session['user_id']
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

        




#add past transactions
@user_cmd_bp.route("/api/past_transactions", methods = ['GET'])
@jwt_required()
def view_past_transactions():
    cursor = None
    db_connection = None
    try:
        #change if we are not using session idk
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized access, login first"}), 401  
        
        # user_id = session['user_id']

        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT order_id, user_id, total_price, total_weight, order_date, order_items
            FROM orders
            WHERE user_id = %s
            ORDER BY order_date DESC
        """, (user_id,))

        transactions = cursor.fetchall()

        for order in transactions:
            order['order_date'] = order['order_date'].isoformat()
            # Parse order_items from JSON if it's stored as string
            if isinstance(order['order_items'], str):
                order['order_items'] = json.loads(order['order_items'])

        return jsonify({"transactions": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

