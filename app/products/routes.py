from flask import Blueprint, request, jsonify
from app import db
from app.products.models import Brand, Category, Product, ProductVariant, Coupon
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload

products_bp = Blueprint('products', __name__)


@products_bp.route('/brands', methods=['POST'])
@jwt_required()
def create_brand():
    try:
        data = request.get_json()
        brand = Brand(name=data['name'])
        db.session.add(brand)
        db.session.commit()
        return jsonify({"message": "Brand created successfully",
                        "brand":{
                            "id" : brand.id,
                            "name": brand.name}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@products_bp.route('/brands', methods=['GET'])
def get_brands():
    try:
        brands = Brand.query.all()
        return jsonify([{"id" : brand.id,
                         "name" : brand.name} for brand in brands]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/brands/<int:id>', methods=['PUT'])
@jwt_required()
def update_brand(id):
    try:
        data = request.get_json()
        brand = Brand.query.get_or_404(id)
        brand.name = data['name']
        db.session.commit()
        return jsonify({"message": "Brand updated successfully",
                        "brand": {
                            "id" : brand.id,
                            "name": brand.name}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/brands/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_brand(id):
    try:
        brand = Brand.query.get_or_404(id)
        db.session.delete(brand)
        db.session.commit()
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.get_json()
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Category created successfully",
                        "category" : {
                            "id" : category.id,
                            "naem" : category.name
                        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([{"id" : category.id,
                        "name" : category.name}
                         for category in categories]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    try:
        data = request.get_json()
        category = Category.query.get_or_404(id)
        category.name = data['name']
        db.session.commit()
        return jsonify({"message": "Category updated successfully",
                        "category" : {
                            "id" : category.id,
                            "name" : category.name
                        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    try:
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        brand = Brand.query.get(data['brand_id'])
        category = Category.query.get(data['category_id'])

        if not brand or not category:
            return jsonify({"error": "Invalid brand or category ID"}), 400
        
        product = Product(
            brand_id=data['brand_id'],
            category_id=data['category_id'],
            name=data['name']
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product created successfully",
                        "Product" : {
                            "id" : product.id,
                            "name" : product.name,
                            "category" : category.name,
                            "brand" : brand.name
                        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        products_list = [{
            "id" : product.id,
            "name" : product.name,
            "category" : product.category.name,
            "brand" : product.brand.name
        } for product in products ]
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    try:
        data = request.get_json()
        product = Product.query.get_or_404(id)
        # product.brand_id = data.get('brand_id', product.brand_id)
        # product.category_id = data.get("category_id", product.category_id)
        product.name = data.get("name", product.name)
        db.session.commit()
        return jsonify({"message": "Product updated successfully",
                        "product" : {
                            "id" : product.id,
                            "name" : product.name,
                            "brand" : product.brand.name,
                            "category" : product.category.name
                        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@products_bp.route('/product_variants', methods=['POST'])
@jwt_required()
def create_product_variant():
    try:
        data = request.get_json()
        product = Product.query.get(data['product_id'])

        if not product:
            return jsonify({"error": "Invalid product ID"}), 400
        
        product_variant = ProductVariant(
            product_id=data['product_id'],
            rating=data.get('rating', 0),
            quantity=data['quantity'],
            description=data['description'],
            price=data['price']
        )
        db.session.add(product_variant)
        db.session.commit()
        return jsonify({"message": "Product variant created successfully",
                        "product_variant" : {
                            "id" : product_variant.id,
                            "name" : product_variant.product.name,
                            "brand" : product_variant.product.brand.name,
                            "category" : product_variant.product.category.name,
                            "price" : product_variant.price,
                            "rating" : product_variant.rating,
                            "quantity" : product_variant.quantity,
                            "description" : product_variant.description
                        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/product_variants', methods=['GET'])
def get_product_variants():
    try:
        sort_by = request.args.get('sort_by', 'name')
        order = request.args.get('order', 'asc')

        valid_sort_fields = ['name', 'rating', 'price', 'quantity']
        if sort_by not in valid_sort_fields:
            return jsonify({"error": "Invalid sort field"}), 400

        valid_order = ['asc', 'desc']
        if order not in valid_order:
            return jsonify({"error": "Invalid order"}), 400
        print(1111111)        
        query = db.session.query(ProductVariant).join(Product).options(joinedload(ProductVariant.product))

        if sort_by == 'name':
            sort_column = Product.name
        else:
            sort_column = getattr(ProductVariant, sort_by)

        if order == 'asc':
            product_variants = query.order_by(sort_column.asc()).all()
        else:
            product_variants = query.order_by(sort_column.desc()).all()

        print(222222)
        product_variants_list = [{
            "id" : product_variant.id,
            "name" : product_variant.product.name,
            "brand" : product_variant.product.brand.name,
            "category" : product_variant.product.category.name,
            "price" : product_variant.price,
            "quantity" : product_variant.quantity,
            "description" : product_variant.description,
            "rating" : product_variant.rating
        } for product_variant in product_variants ]

        return jsonify(product_variants_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/product_variants/<int:id>', methods=['PUT'])
@jwt_required()
def update_product_variant(id):
    try:
        data = request.get_json()
        product_variant = ProductVariant.query.get_or_404(id)
        # product_variant.product_id = data['product_id']
        product_variant.rating = data.get('rating', product_variant.rating)
        product_variant.quantity = data.get('quantity', product_variant.quantity)
        # product_variant.description = data['description']
        product_variant.price = data.get('price', product_variant.price)
        db.session.commit()
        return jsonify({"message": "Product variant updated successfully",
                        "details" : {
                            "id" : product_variant.id,
                            "name" : product_variant.product.name,
                            "brand" : product_variant.product.brand.name,
                            "category" : product_variant.product.category.name,
                            "price" : product_variant.price,
                            "quantity" : product_variant.quantity,
                            "description" : product_variant.description,
                            "rating" : product_variant.rating
                        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/product_variants/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product_variant(id):
    try:
        product_variant = ProductVariant.query.get_or_404(id)
        db.session.delete(product_variant)
        db.session.commit()
        return jsonify({"message": "Product variant deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@products_bp.route('/coupons', methods=['POST'])
def create_coupon():
    try:
        data = request.get_json()
        coupon = Coupon(
            code=data['code'],
            discount=data['discount'],
            active=data['active']
        )
        db.session.add(coupon)
        db.session.commit()
        return jsonify({"message": "Coupon created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@products_bp.route('/coupons', methods=['GET'])
def get_coupons():
    try:
        coupons = Coupon.query.all()
        return jsonify([{"id": coupon.id, "code": coupon.code} for coupon in coupons]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/coupons/<int:id>', methods=['PUT'])
def update_coupon(id):
    try:
        data = request.get_json()
        coupon = Coupon.query.get_or_404(id)
        coupon.code = data['code']
        coupon.discount = data['discount']
        coupon.active = data['active']
        db.session.commit()
        return jsonify({"message": "Coupon updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@products_bp.route('/coupons/<int:id>', methods=['DELETE'])
def delete_coupon(id):
    try:
        coupon = Coupon.query.get_or_404(id)
        db.session.delete(coupon)
        db.session.commit()
        return jsonify({"message": "Coupon deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
