from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_object("app.config.Config")

    # Inits
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from app.controllers.auth import bp as AuthenticationBlueprint
    api.register_blueprint(AuthenticationBlueprint)

    return app
