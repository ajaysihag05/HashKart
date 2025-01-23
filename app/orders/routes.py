from flask import Blueprint, request, jsonify
from app import db
from app.orders.models import Order, OrderItem, Payment
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.users.models import Cart, CartItem
from app.products.models import Product, ProductVariant, Coupon


orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity()
        coupon_code = request.get_json().get('coupon_code')

        cart = Cart.query.filter_by(user_id = user_id).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400
        
        # Calculate the total price
        total_price = 0
        for item in cart_items:
            product_variant = ProductVariant.query.get(item.product_variant_id)
            total_price += product_variant.price * item.quantity
        
        # Apply coupon if provided
        discount = 0
        if coupon_code:
            coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
            if coupon:
                discount = total_price * (coupon.discount / 100)
                total_price -= discount
            else:
                return jsonify({"error": "Invalid or expired coupon"}), 400
    
        # Create the order
        order = Order(user_id=user_id, total_price=total_price, coupon_id=coupon.id if coupon_code else None)
        db.session.add(order)
        db.session.commit()

        # Create order items
        for item in cart_items:
            product_variant = ProductVariant.query.get(item.product_variant_id)
            order_item = OrderItem(order_id=order.id, product_variant_id=product_variant.id, quantity=item.quantity, price=product_variant.price)
            db.session.add(order_item)

        db.session.commit()

        return jsonify({"message": "Order created successfully", "order_id": order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
