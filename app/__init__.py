from flask import Flask
from .extensions import db, jwt
from .auth.routes import auth_bp
from .expenses.routes import expenses_bp
from .reports.routes import reports_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/ExpenseTracker'

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app
