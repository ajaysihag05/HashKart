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
            coupon = Coupon.query.filter_by(code=coupon_code, active=True).first()
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
        print(111111)
        for item in cart_items:
            product_variant = ProductVariant.query.get(item.product_variant_id)
            order_item = OrderItem(order_id=order.id, product_variant_id=product_variant.id, quantity=item.quantity, price=product_variant.price)
            db.session.add(order_item)
            db.session.delete(item)
        db.session.commit()
        print(22222)
        order_items = OrderItem.query.filter_by(order_id = order.id).all()
        order_items_list = [{
            "order_item_id": ord_item.id,
            "item_name":ord_item.product_variant.product.name,
            "item_price":ord_item.product_variant.price
        } for ord_item in order_items]
        print(33333)
        db.session.commit()

        return jsonify({"message": "Order created successfully",
                        "details" : {
                            "order_id" : order.id,
                            "price" : order.total_price,
                            "status" : order.status,
                            "order_items" : order_items_list
                        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@orders_bp.route('/payment', methods=['POST'])
@jwt_required()
def make_payment():
    order_id = request.json.get('order_id')
    # amount = request.json.get('amount')
    payment_method = request.json.get('payment_method')

    try:
        # Fetch the order
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Process the payment (dummy processing for example)
        payment = Payment(order_id=order.id, amount=order.total_price, payment_method=payment_method, status='Completed')
        db.session.add(payment)

        # Update order status
        order.status = 'Completed'
        db.session.commit()

        return jsonify({"message": "Payment processed successfully",
                        "details": {
                            "id" : payment.id,
                            "status" : payment.status,
                            "amount" : payment.amount
                        }}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500