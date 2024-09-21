from app.extensions import db


class InformacaoNutricional(db.Model):
    __tablename__ = 'informacoes_nutricionais'
    __table_args__ = {'schema': 'public'}

    info_nutricional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alimento_id = db.Column(db.Integer, db.ForeignKey('public.alimento.alimento_id'))

    proteina = db.Column(db.Numeric(10, 2))
    carboidrato = db.Column(db.Numeric(10, 2))
    lipidio = db.Column(db.Numeric(10, 2))
    fibra = db.Column(db.Numeric(10, 2))
    calorias = db.Column(db.Integer)
    vitaminac = db.Column(db.Numeric(10, 2))
    calcio = db.Column(db.Numeric(10, 2))
    ferro = db.Column(db.Numeric(10, 2))
    sodio = db.Column(db.Numeric(10, 2))

    alimento = db.relationship('Alimento', foreign_keys=[alimento_id])

    def __repr__(self):
        return f'<InformacaoNutricional {self.info_nutricional_id}>'

    def to_dict(self):
        return {
            'alimento_id': self.alimento_id,
            'proteina': float(self.proteina) if self.proteina is not None else None,
            'carboidrato': float(self.carboidrato) if self.carboidrato is not None else None,
            'lipidio': float(self.lipidio) if self.lipidio is not None else None,
            'fibra': float(self.fibra) if self.fibra is not None else None,
            'calorias': self.calorias,
            'vitaminac': float(self.vitaminac) if self.vitaminac is not None else None,
            'calcio': float(self.calcio) if self.calcio is not None else None,
            'ferro': float(self.ferro) if self.ferro is not None else None,
            'sodio': float(self.sodio) if self.sodio is not None else None,
        }