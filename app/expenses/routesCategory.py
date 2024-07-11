from flask import request, jsonify
from .models import Category
from .schemas import category_schema, categories_schema
from app.extensions import db
from flask_jwt_extended import jwt_required
from . import categories_bp

@categories_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories))

@categories_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    name = request.form['name']
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201

@categories_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    name = request.form
    category.name = name.get('name',None)
    db.session.commit()
    return jsonify(category_schema.dump(category))

@categories_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"})
