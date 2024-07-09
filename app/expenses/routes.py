from flask import request, jsonify
from .models import Expense
from .schemas import expense_schema, expenses_schema
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
