from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    from app.users import bp as users_bp
    from app.models_bp import bp as models_bp
    from app.origins import bp as origins_bp
    from app.destinations import bp as destinations_bp
    from app.costs import bp as costs_bp
    from app.results import bp as results_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(models_bp, url_prefix='/models')
    app.register_blueprint(origins_bp, url_prefix='/origins')
    app.register_blueprint(destinations_bp, url_prefix='/destinations')
    app.register_blueprint(costs_bp, url_prefix='/costs')
    app.register_blueprint(results_bp, url_prefix='/results')

    from app.main_routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app.models import User, TransportModel, Origin, Destination, Cost, ResultHeader, ResultDetail  # noqa
