from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import timedelta


#Import area for the FLASK blue print
from auth import auth_bp
from searchbar import search_bp
from creditcard_check import credit_card_bp
from cart import cart_bp
from user_command import user_cmd_bp
from admin_command import admin_cmd_bp


app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins=["http://localhost:5173"])





#all of these are global for the app
#remove is its messing stuff up
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Use True only if running on HTTPS
app.config['SECRET_KEY'] = 'testkey'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Prevent cross-site request issues
#the thing not working properly when samesite is set to lax we need to read more on documentation to figure out why
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # Default session lifetime



#register all future API end points here
app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(credit_card_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_cmd_bp)
app.register_blueprint(admin_cmd_bp)

#health check to test if your are unsure API is working
@app.route("/api/healthcheck", methods=['GET'])
def health_check():
    return {"status": "API is working!"}, 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)