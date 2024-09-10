from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from Config import Config
from app.extensions import db
from app.main import bp as main_bp
from app.auth import bp as auth_bp
from app.routes.alimento_routes import alimentos_bp
from app.routes.tipo_alimento_routes import bp as tipo_alimento_bp
from app.models.usuarios import Usuario

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    # Initialize Flask extensions
    db.init_app(app)

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # A rota para login

    # Register blueprints

    app.register_blueprint(main_bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.register_blueprint(tipo_alimento_bp, url_prefix='/api')

    app.register_blueprint(alimentos_bp, url_prefix='/api')

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    CORS(app)

    return app
