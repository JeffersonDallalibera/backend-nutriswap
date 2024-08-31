from app.extensions import db
from werkzeug.security import check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'public'}

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(256))  # Ajustado para 256

    def __repr__(self):
        return f'<Usuario {self.username}>'

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password)

    @property
    def is_active(self) -> bool:
        # Usuários são sempre ativos
        return True

    @property
    def is_authenticated(self) -> bool:
        # Verifica se o usuário está autenticado
        return True

    @property
    def is_anonymous(self) -> bool:
        # Usuários nunca são anônimos
        return False

    def get_id(self) -> str:
        # Retorna o ID do usuário como string
        return str(self.user_id)
