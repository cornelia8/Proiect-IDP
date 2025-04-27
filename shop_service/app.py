# app.py
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from config import DATABASE_URI
from database import db
from models import Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
metrics = PrometheusMetrics(app)

@app.route('/health')
def health_check():
    return "Shop Service is running!"

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'seller': item.seller
    } for item in items])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = Item(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        seller=data['seller']   # Seller now enforced by Gateway JWT
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'seller': item.seller
        })
    else:
        return jsonify({'error': 'Item not found'}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)
