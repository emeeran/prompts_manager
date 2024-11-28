from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Database configuration
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("No DATABASE_URL set in environment")

    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DEBUG=True  # Enable debug mode
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Import models here to avoid circular imports
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        db.create_all()

        # Register blueprints
        from .auth import auth
        from .main import main

        app.register_blueprint(auth)
        app.register_blueprint(main)

        # Ensure templates directory exists
        os.makedirs(app.template_folder, exist_ok=True)

        # Add debug route
        @app.route('/debug')
        def debug():
            return 'Debug page working'

    return app
