from marshmallow import Schema, fields

class ExpenseSchema(Schema):
    amount = fields.Float(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True)
    date = fields.Date()

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
