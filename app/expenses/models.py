from app.extensions import db
from datetime import datetime


# Association table for many-to-many relationship between Expense and Category
expense_category = db.Table('expense_category',
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.relationship(Category, secondary=expense_category, lazy='subquery',
                                 backref=db.backref('expenses', lazy=True))
