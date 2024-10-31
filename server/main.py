from flask import Flask, jsonify, request
from flask_cors import CORS
from auth import auth_bp
from searchbar import search_bp


app = Flask(__name__)
cors = CORS(app, origins="*")

app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)

@app.route("/api/healthcheck", methods=['GET'])
def health_check():
    return {"status": "API is working!"}, 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)