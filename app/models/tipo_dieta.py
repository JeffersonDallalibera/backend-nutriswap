
from app.extensions import db

class TipoDieta(db.Model):
    __tablename__ = 'tipo_dieta'
    __table_args__ = {'schema': 'NutriSwap'}

    tipo_dieta_id = db.Column(db.Integer, primary_key=True)
    nome_tipo_dieta = db.Column(db.String(50))

    def __repr__(self):
        return f'<TipoDieta {self.nome_tipo_dieta}>'
