# models/pessoa.py
from app import db

class PessoaDieta(db.Model):
    __tablename__ = 'pessoa'
    __table_args__ = {'schema': 'public'}

    id_pessoa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_pessoa = db.Column(db.String(100), nullable=False)
    idade_pessoa = db.Column(db.Integer, nullable=False)
    peso_pessoa = db.Column(db.Numeric(6, 2), nullable=False)  # Peso em kg
    altura_pessoa = db.Column(db.Integer, nullable=False)  # Altura em cm
    email_pessoa = db.Column(db.String(100), nullable=False)
    telefone_pessoa = db.Column(db.String(20))
    imc_pessoa = db.Column(db.Numeric(5, 2))  # IMC calculado

    # Campos de restrições alimentares
    vegetariano = db.Column(db.Boolean, default=False)
    intolerante_lactose = db.Column(db.Boolean, default=False)
    alergia_nozes = db.Column(db.Boolean, default=False)
    alergia_gluten = db.Column(db.Boolean, default=False)
    alergia_mariscos = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Pessoa {self.nome_pessoa}>'

    def to_dict(self):
        return {
            'id_pessoa': self.id_pessoa,
            'nome_pessoa': self.nome_pessoa,
            'idade_pessoa': self.idade_pessoa,
            'peso_pessoa': self.peso_pessoa,
            'altura_pessoa': self.altura_pessoa,
            'email_pessoa': self.email_pessoa,
            'telefone_pessoa': self.telefone_pessoa,
            'imc_pessoa': self.imc_pessoa,
            'vegetariano': self.vegetariano,
            'intolerante_lactose': self.intolerante_lactose,
            'alergia_nozes': self.alergia_nozes,
            'alergia_gluten': self.alergia_gluten,
            'alergia_mariscos': self.alergia_mariscos,
        }
