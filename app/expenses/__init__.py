from flask import Blueprint

expenses_bp = Blueprint('expenses', __name__)
categories_bp = Blueprint('categories', __name__)
from . import routesExpenses
from . import routesCategory
