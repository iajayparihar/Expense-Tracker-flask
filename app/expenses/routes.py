from flask import request, jsonify
from .models import Expense
from .schemas import expenses_schema, expense_schema
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import expenses_bp

@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    expenses_data = expenses_schema.dump(expenses)
    return jsonify(expenses_data)


@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    amount = request.form['amount']
    desc = request.form['description']
    category = request.form['category']
    user_id = get_jwt_identity()

    expense = Expense(user_id=user_id, amount=amount, description = desc, category = category)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"payload": "data saved."}), 201



@expenses_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(user_id=user_id, id=id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify(expense_schema.dump(expense))


@expenses_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(user_id=user_id, id=id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.form
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    expense.category = data.get('category', expense.category)
    db.session.commit()
    return jsonify(expense_schema.dump(expense))


@expenses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(user_id=user_id, id=id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"}), 200

@expenses_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    summary = {}
    for expense in expenses:
        category = expense.category
        if category not in summary:
            summary[category] = 0
        summary[category] += expense.amount

    return jsonify(summary)