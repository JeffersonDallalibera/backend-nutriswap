from app.extensions import db

class PesquisaUsuario(db.Model):
    __tablename__ = 'pesquisa_usuario'
    __table_args__ = {'schema': 'NutriSwap'}

    pesquisa_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.usuarios.user_id'))
    data_pesquisa = db.Column(db.Date)

    usuario = db.relationship('Usuario', backref=db.backref('pesquisas', lazy=True))

    def __repr__(self):
        return f'<PesquisaUsuario {self.pesquisa_id}>'

