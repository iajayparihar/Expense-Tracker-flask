from flask import jsonify
from app.expenses.models import Expense
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql import func
from . import reports_bp

@reports_bp.route('/monthly/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def get_monthly_report(year, month):
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).filter(
        func.extract('year', Expense.date) == year,
        func.extract('month', Expense.date) == month
    ).all()
    total_amount = sum(expense.amount for expense in expenses)
    return jsonify({
        'month': f'{year}-{month:02}',
        'total_amount': total_amount,
        'expenses': [{'id': exp.id, 'amount': exp.amount, 'description': exp.description, 'category': exp.category, 'date': exp.date} for exp in expenses]
    })

@reports_bp.route('/annual/<int:year>', methods=['GET'])
@jwt_required()
def get_annual_report(year):
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).filter(
        func.extract('year', Expense.date) == year
    ).all()
    total_amount = sum(expense.amount for expense in expenses)
    return jsonify({
        'year': f'{year}',
        'total_amount': total_amount,
        'expenses': [{'id': exp.id, 'amount': exp.amount, 'description': exp.description, 'category': exp.category, 'date': exp.date} for exp in expenses]
    })
