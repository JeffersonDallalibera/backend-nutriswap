
from app.extensions import db

class PreferenciaUsuario(db.Model):
    __tablename__ = 'preferencias_usuario'
    __table_args__ = {'schema': 'NutriSwap'}

    user_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.usuarios.user_id'), primary_key=True)
    vegetariano = db.Column(db.Boolean)
    intolerante_lactose = db.Column(db.Boolean)
    alergia_nozes = db.Column(db.Boolean)
    alergia_gluten = db.Column(db.Boolean)
    alergia_mariscos = db.Column(db.Boolean)
    preferencia_organico = db.Column(db.Boolean)
    tipo_dieta_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.tipo_dieta.tipo_dieta_id'))
    objetivo_saude = db.Column(db.String(100))
    necessidades_nutricionais = db.Column(db.String(200))
    nivel_atividade = db.Column(db.String(50))

    usuario = db.relationship('Usuario', backref=db.backref('preferencias', uselist=False))
    tipo_dieta = db.relationship('TipoDieta', backref=db.backref('preferencias', lazy=True))

    def __repr__(self):
        return f'<PreferenciaUsuario {self.user_id}>'
