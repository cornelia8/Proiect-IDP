# app.py
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from config import DATABASE_URI
from database import db
from models import Transaction
from datetime import datetime
import requests
import jwt  # make sure it's imported

SECRET_KEY = 'parolasecreta'  # same secret as user_service and api_gateway

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
metrics = PrometheusMetrics(app)

@app.route('/health')
def health_check():
    return "Transaction Service is running!"

@app.route('/transactions', methods=['GET'])
def get_transactions():
    token = None
    if 'Authorization' in request.headers:
        bearer = request.headers['Authorization']
        token = bearer.split()[1] if bearer.startswith('Bearer ') else None

    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = data['username']
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

    # Only show transactions where user is the buyer (we can later extend to seller if we want)
    transactions = Transaction.query.filter_by(buyer=username).all()

    return jsonify([{
        'id': t.id,
        'buyer': t.buyer,
        'seller': t.seller,
        'item_name': t.item_name,
        'price': t.price,
        'timestamp': t.timestamp.isoformat()
    } for t in transactions])

@app.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.json
    buyer = data.get('buyer')
    item_id = data.get('item_id')

    if not buyer or not item_id:
        return jsonify({"error": "Missing buyer or item_id"}), 400

    # Fetch item details from shop_service
    try:
        response = requests.get(f'http://shop-service:5002/items/{item_id}', timeout=5)
        if response.status_code != 200:
            return jsonify({"error": "Item not found"}), 404
        item_data = response.json()
    except requests.exceptions.RequestException:
        return jsonify({"error": "Shop Service unavailable"}), 503

    # Create transaction
    transaction = Transaction(
        buyer=buyer,
        seller=item_data['seller'],
        item_name=item_data['name'],
        price=item_data['price']
    )

    db.session.add(transaction)
    db.session.commit()

    # Delete item from shop after purchase
    try:
        requests.delete(f'http://shop-service:5002/items/{item_id}', timeout=5)
    except requests.exceptions.RequestException:
        pass

    return jsonify({'message': 'Transaction recorded successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()     # Drop tables (dev mode, no modifica/decomenta)
        db.create_all()   # Create tables
    app.run(host='0.0.0.0', port=5003)
