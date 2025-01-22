from flask import Blueprint, request, jsonify
from app import db
from app.orders.models import Order, OrderItem, Payment

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        user_id = data['user_id']
        total_price = data['total_price']
        status = data['status']
        order = Order(user_id=user_id, total_price=total_price, status=status)
        db.session.add(order)
        db.session.commit()
        return jsonify({"message": "Order created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
