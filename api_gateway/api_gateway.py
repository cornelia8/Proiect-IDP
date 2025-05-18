from flask import Flask, request, jsonify
import requests
import jwt
from functools import wraps
from prometheus_flask_exporter import PrometheusMetrics  # ✅ Metrics

app = Flask(__name__)
SECRET_KEY = 'parolasecreta'  # Same as in user_service

# ✅ Initialize metrics
metrics = PrometheusMetrics(app)

USER_SERVICE_URL = "http://user-service:5001"
SHOP_SERVICE_URL = "http://shop-service:5002"
TRANSACTION_SERVICE_URL = "http://transaction-service:5003"

# JWT helper
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer.split()[1] if bearer.startswith('Bearer ') else None

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

# Helper to forward requests
def forward_request(service_url, method="GET", json_data=None, headers=None):
    try:
        if method == "POST":
            response = requests.post(service_url, json=json_data, headers=headers, timeout=5)
        elif method == "DELETE":
            response = requests.delete(service_url, headers=headers, timeout=5)
        else:
            response = requests.get(service_url, headers=headers, timeout=5)

        return (response.content, response.status_code, response.headers.items())

    except requests.exceptions.RequestException:
        return jsonify({"error": f"Service unavailable at {service_url}"}), 503

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Marketplace API Gateway! 🚀"})

# Health Check
@app.route('/health')
def health():
    return jsonify({"status": "API Gateway is running!"})

# Error Handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

# AUTH Routes
@app.route('/signup', methods=['POST'])
def signup():
    return forward_request(f"{USER_SERVICE_URL}/signup", method="POST", json_data=request.get_json())

@app.route('/login', methods=['POST'])
def login():
    return forward_request(f"{USER_SERVICE_URL}/login", method="POST", json_data=request.get_json())

# USERS
@app.route('/users', methods=['GET'])
@app.route('/users/<path:path>', methods=['GET'])
def users_proxy(path=""):
    url = f"{USER_SERVICE_URL}/users"
    if path:
        url += f"/{path}"
    return forward_request(url, method=request.method)

# ITEMS
@app.route('/items', methods=['GET'])
def items_public():
    return forward_request(f"{SHOP_SERVICE_URL}/items")

@app.route('/items', methods=['POST'])
@token_required
def items_post():
    data = request.get_json()
    data['seller'] = request.current_user  # Force seller from token
    return forward_request(f"{SHOP_SERVICE_URL}/items", method="POST", json_data=data)

@app.route('/items/<path:path>', methods=['GET', 'DELETE'])
def items_by_id_proxy(path=""):
    url = f"{SHOP_SERVICE_URL}/items/{path}"
    return forward_request(url, method=request.method)

# TRANSACTIONS
@app.route('/transactions', methods=['POST'])
@token_required
def transactions_post():
    data = request.get_json()
    data['buyer'] = request.current_user  # Force buyer from token
    return forward_request(f"{TRANSACTION_SERVICE_URL}/transactions", method="POST", json_data=data)

@app.route('/transactions', methods=['GET'])
@token_required
def transactions_get():
    headers = {"Authorization": request.headers.get("Authorization")}
    return forward_request(f"{TRANSACTION_SERVICE_URL}/transactions", method="GET", headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
