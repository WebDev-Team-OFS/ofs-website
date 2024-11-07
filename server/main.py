from flask import Flask, jsonify, request
from flask_cors import CORS



#Import area for the FLASK blue print
from auth import auth_bp
from searchbar import search_bp
from credit_check import credit_card_bp

app = Flask(__name__)
cors = CORS(app, origins="*")


#register all future API end points here
app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(credit_card_bp)

#health check to test if your are unsure API is working
@app.route("/api/healthcheck", methods=['GET'])
def health_check():
    return {"status": "API is working!"}, 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)