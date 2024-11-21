from flask import Blueprint, jsonify, request
from db_module import get_db_connection

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search", methods=["GET"])
def search_products():
    try:
        # Get search query from request arguments
        query = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()
        
         # Validate input to prevent SQL injection (remove unwanted characters)
        if not all(c.isalnum() or c.isspace() for c in query) or not all(c.isalnum() or c.isspace() for c in category):
            return jsonify({"error": "Invalid characters detected in query or category!"}), 400


        # Connect to the database
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        #need to fix query also to stop so many server requests
        #updated here to take in both catgory and normal search
        if query and category:
            search_query = f"%{query}%"
            category_query = f"%{category}"
            cursor.execute("""
            SELECT product_id, name, brand, stock, price, weight, category, description
            FROM product
            WHERE (name LIKE %s or brand LIKE %s) AND category LIKE %s
            """, (search_query, search_query, category_query))
        elif query:       
        # Search for products by name or category 
            search_query = f"%{query}%"
            cursor.execute("""
            SELECT product_id, name, brand, stock, price, weight, category, description
            FROM product
            WHERE name LIKE %s OR category LIKE %s OR brand LIKE %s
            """, (search_query, search_query, search_query))
        elif category:
            category_query = f"%{category}%"
            cursor.execute("""
            SELECT product_id, name, brand, stock, price, weight, category, description
            FROM product
            WHERE name LIKE %s OR category LIKE %s OR brand LIKE %s
            """, (category_query, category_query, category_query))
        else:
            cursor.execute("""SELECT * FROM product """)

        # Fetch all matching products
        products = cursor.fetchall()
        
        cursor.close()
        db_connection.close()

        # Return the matching products as a JSON response
        return jsonify({"products": products})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
    



@search_bp.route("/api/product/<int:product_id>", methods=["GET"])
def click_product(product_id):
    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)


        cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        db_connection.close()

        if product:
            return jsonify({"product": product}), 200
        else:
            return jsonify({"error": "product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

