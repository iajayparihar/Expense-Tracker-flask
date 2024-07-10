from flask import request, jsonify
from .models import Expense, Category
from .schemas import expenses_schema, expense_schema
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import expenses_bp


@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify(expenses_schema.dump(expenses))


@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    amount = request.form['amount']
    desc = request.form['description']
    category_ids = request.form['category_ids']
    user_id = get_jwt_identity()

    # Convert category_ids to a list of integers
    category_ids = [int(id) for id in category_ids.split(',')]

    categories = Category.query.filter(Category.id.in_(category_ids)).all()
    expense = Expense(user_id=user_id, amount=amount, description=desc, categories=categories)
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 201


@expenses_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify(expense_schema.dump(expense))


@expenses_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.form
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    category_ids = data.get('category_ids', None)

    if category_ids:
        expense.categories = Category.query.filter(Category.id.in_(category_ids)).all()

    db.session.commit()
    return jsonify(expense_schema.dump(expense))


@expenses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"})


@expenses_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    summary = {}

    for expense in expenses:
        for category in expense.categories:
            if category.name not in summary:
                summary[category.name] = 0
            summary[category.name] += expense.amount

    return jsonify(summary)