from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import settings
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
    app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
    app.static_folder = 'static'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"
    login_manager.login_message_category = "info"

    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)
    
    from .models import User, Post, Vote
    
    with app.app_context():
        db.create_all()
    

    return app

