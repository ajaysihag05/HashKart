from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.users.models import User, Cart, CartItem
from app.products.models import Product, ProductVariant


users_bp = Blueprint('users', __name__)

@users_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id))
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return jsonify(username=user.username, email=user.email), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route('/carts', methods=['POST'])
@jwt_required()
def create_cart():
    try:
        user_id = get_jwt_identity()
        existing_cart = Cart.query.filter_by(user_id=user_id).first()
        if existing_cart:
            return jsonify({"message": "A cart already exists for this user"}), 400
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        return jsonify({"message": "Cart created successfully",
                        "details" : {
                            "id" : cart.id,
                            "user Id" : cart.user_id,
                            "username" : cart.user.username
                        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@users_bp.route('/cart_items', methods=['POST'])
@jwt_required()
def add_cart_item():
    try:
        user_id = get_jwt_identity()
        cart = Cart.query.filter_by(user_id=user_id).first()
        data = request.get_json()
        if not cart:
            return jsonify({"message": "No cart exists for this user, Please create one"}), 400
        product_variant = ProductVariant.query.filter_by(id = data["product_variant_id"]).first()
        if not product_variant:
            return jsonify({"message": "Sorry there is no such product variant with this ID"})
        cart_item = CartItem(
            cart_id=cart.id,
            product_variant_id=data['product_variant_id'],
            quantity=data['quantity']
        )
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Item added successfully",
                        "details":{
                            "name" : cart_item.product_variant.product.name,
                            "quantity" : cart_item.quantity,
                            "price" : cart_item.product_variant.price
                        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@users_bp.route('/cart_items', methods=['GET'])
@jwt_required()
def get_cart_items():
    try:
        user_id = get_jwt_identity()
        cart = Cart.query.filter_by(user_id=user_id).first()
        cart_items = CartItem.query.filter_by(cart_id = cart.id).all()
        cart_items_data = [{
            "id" : cart_item.id,
            "name" : cart_item.product_variant.product.name,
            "quantity" : cart_item.quantity,
            "price" : cart_item.product_variant.price
        } for cart_item in cart_items]

        return jsonify(cart_items_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@users_bp.route('/cart_items/<int:id>', methods=['PUT'])
@jwt_required()
def update_cart_item_quantity(id):
    try:
        data = request.get_json()
        cart_item = CartItem.query.get_or_404(id)
        cart_item.quantity = data.get('quantity', cart_item.quantity)
        db.session.commit()
        return jsonify({"message": "Cart item quantity updated successfully",
                        "details" : {
                            "id" : cart_item.id,
                            "name" : cart_item.product_variant.product.name,
                            "quantity" : cart_item.quantity
                        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@users_bp.route('/cart_items/<int:id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(id):
    try:
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400