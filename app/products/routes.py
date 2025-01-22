from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.products.models import Product, ProductVariant, Cart, CartItem

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        product_variant_id = data['product_variant_id']
        quantity = data['quantity']
        
        cart = Cart.query.filter_by(user_id=user_id, status='active').first()
        if not cart:
            cart = Cart(user_id=user_id, status='active')
            db.session.add(cart)
            db.session.commit()
        
        cart_item = CartItem(cart_id=cart.id, product_variant_id=product_variant_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        
        cart.update_amount()
        
        return jsonify({"message": "Item added to cart"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@products_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        cart = Cart.query.filter_by(user_id=user_id, status='active').first()
        if not cart:
            return jsonify({"message": "Cart is empty"}), 200

        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        items = [{"product_variant_id": item.product_variant_id, "quantity": item.quantity} for item in cart_items]
        
        return jsonify({"cart": {"id": cart.id, "amount": cart.amount, "items": items}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
