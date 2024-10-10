from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate

from app.Config import Config  # Certifique-se de que o nome está correto
from app.extensions import db
from app.main import bp as main_bp
from app.auth import bp as auth_bp
from app.routes.alimento_routes import alimentos_bp
from app.routes.nutricao_routes import nutricao_bp
from app.routes.tipo_alimento_routes import bp as tipo_alimento_bp
from app.models.usuarios import Usuario
from app.routes.pessoa_routes import bp as pessoa_bp
from app.routes.pdf_routes import bp as pdf_bp
from dotenv import load_dotenv  # Importar para carregar variáveis de ambiente

# Adicionando instância de Migrate
migrate = Migrate()


def create_app(config_class=Config):
    load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)  # Inicializar o Flask-Migrate

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # A rota para login

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tipo_alimento_bp, url_prefix='/api')
    app.register_blueprint(alimentos_bp, url_prefix='/api')
    app.register_blueprint(nutricao_bp, url_prefix='/api')
    app.register_blueprint(pessoa_bp, url_prefix='/api')
    app.register_blueprint(pdf_bp, url_prefix='/api')

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Habilitar CORS
    CORS(app)

    return app
