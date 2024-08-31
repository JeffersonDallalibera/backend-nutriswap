from app.extensions import db

class AlimentoPesquisa(db.Model):
    __tablename__ = 'alimentos_pesquisa'
    __table_args__ = {'schema': 'NutriSwap'}

    alimento_pesquisa_id = db.Column(db.Integer, primary_key=True)
    pesquisa_id = db.Column(db.Integer, db.ForeignKey('NutriSwap.pesquisa_usuario.pesquisa_id'))
    alimento_trocar = db.Column(db.String(100))
    alimento_selecionado = db.Column(db.String(100))

    pesquisa_usuario = db.relationship('PesquisaUsuario', backref=db.backref('alimentos_pesquisa', lazy=True))

    def __repr__(self):
        return f'<AlimentoPesquisa {self.alimento_pesquisa_id}>'

