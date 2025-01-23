from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    products = db.relationship('Product', backref='brand', lazy=True)


    __table_args__ = (
        UniqueConstraint('name', name='uq_brand_name'),
    )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)


    __table_args__ = (
        UniqueConstraint('name', name='uq_category_name'),
    )

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    product_variants = db.relationship("ProductVariant", backref="product", lazy=True)

    __table_args__ = (
        UniqueConstraint('name', name='uq_product_name'),
    )

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_property_name'),
    )

class ProductVariant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cart_item = db.relationship("CartItem", backref="product_variant", lazy=True)

class ProductVariantProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    value = db.Column(db.String(150), nullable=False)

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    discount = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
