
from app.extensions import db

class TipoAlimento(db.Model):
    __tablename__ = 'tipo_alimento'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f'<TipoAlimento {self.nome}>'
