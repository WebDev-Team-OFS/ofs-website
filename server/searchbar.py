from flask import Blueprint, jsonify, request
from db_module import get_db_connection

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search", methods=["GET"])
def search_products():
    try:
        # Get search query from request arguments
        query = request.args.get("query", "").strip()
        
        # Connect to the database
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        if query:       
        # Search for products by name or category 
            search_query = f"%{query}%"
            cursor.execute("""
            SELECT product_id, name, brand, stock, price, weight, category, description
            FROM product
            WHERE name LIKE %s OR category LIKE %s
            """, (search_query, search_query))
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