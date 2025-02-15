from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Set the login view

    # Create database tables
    with app.app_context():
        db.create_all()

    return app