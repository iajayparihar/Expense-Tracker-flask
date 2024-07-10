from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from .models import Category, Expense

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True

class ExpenseSchema(SQLAlchemyAutoSchema):
    categories = fields.List(fields.Nested(CategorySchema))
    class Meta:
        model = Expense
        include_relationships = True
        load_instance = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
