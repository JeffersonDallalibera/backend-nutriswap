from app.extensions import db

class InformacaoNutricional(db.Model):
    __tablename__ = 'informacoes_nutricionais'
    __table_args__ = {'schema': 'NutriSwap'}

    info_nutricional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alimento_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.alimentos.alimento_id'))
    proteina = db.Column(db.Numeric(10, 2))
    carboidrato = db.Column(db.Numeric(10, 2))
    lipidio = db.Column(db.Numeric(10, 2))
    fibra = db.Column(db.Numeric(10, 2))
    calorias = db.Column(db.Integer)
    vitaminac = db.Column(db.Numeric(10, 2))
    calcio = db.Column(db.Numeric(10, 2))
    ferro = db.Column(db.Numeric(10, 2))
    sodio = db.Column(db.Numeric(10, 2))

    alimento = db.relationship('Alimento', backref=db.backref('informacoes_nutricionais', uselist=False))


    def __repr__(self):
        return f'<InformacaoNutricional {self.info_nutricional_id}>'
