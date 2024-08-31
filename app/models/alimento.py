from app.extensions import db


class Alimento(db.Model):
    __tablename__ = 'alimentos'
    __table_args__ = {'schema': 'NutriSwap'}

    alimento_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.tipo_alimento.tipo_id'))

    tipo_alimento = db.relationship('TipoAlimento', backref=db.backref('alimentos', lazy=True))

    def __repr__(self):
        return f'<Alimento {self.nome}>'

