# models/alimento.py
from app import db


class Alimento(db.Model):
    __tablename__ = 'alimento'
    __table_args__ = {'schema': 'public'}

    alimento_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo_alimento_id = db.Column(db.Integer, db.ForeignKey('public.tipo_alimento.id'))

    tipo_alimento = db.relationship('TipoAlimento', backref=db.backref('alimentos', lazy=True))

    def __repr__(self):
        return f'<Alimento {self.nome}>'

    def to_dict(self):
        return {
            'alimento_id': self.alimento_id,
            'nome': self.nome,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'tipo_alimento_id': self.tipo_alimento_id,
            'tipo_alimento': self.tipo_alimento.nome if self.tipo_alimento else None
        }
