from app import db
from app.models.pessoa import PessoaDieta
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.exc import SQLAlchemyError

def inserir_pessoa(pessoa_data):
    try:
        nova_pessoa = PessoaDieta(
            nome_pessoa=pessoa_data['nome'],
            idade_pessoa=pessoa_data['idade'],
            peso_pessoa=pessoa_data['peso'],
            altura_pessoa=pessoa_data['altura'],  # Grava em cm
            email_pessoa=pessoa_data['email'],
            telefone_pessoa=pessoa_data['telefone'],
            imc_pessoa=pessoa_data.get('imc_pessoa'),  # Aceita o IMC do frontend
            vegetariano=pessoa_data.get('restricoes', {}).get('vegetariano', False),
            intolerante_lactose=pessoa_data.get('restricoes', {}).get('intoleranteLactose', False),
            alergia_nozes=pessoa_data.get('restricoes', {}).get('alergiaNozes', False),
            alergia_gluten=pessoa_data.get('restricoes', {}).get('alergiaGluten', False),
            alergia_mariscos=pessoa_data.get('restricoes', {}).get('alergiaMariscos', False),
        )

        db.session.add(nova_pessoa)
        db.session.commit()
        return nova_pessoa.to_dict()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def buscar_todas_pessoas():
    try:
        pessoas = PessoaDieta.query.all()
        return [pessoa.to_dict() for pessoa in pessoas]
    except SQLAlchemyError as e:
        raise e


def criar_pessoa_pdf(idPessoa):
    try:
        print(str(idPessoa) + "->idPessoa")

        # Obtém a primeira pessoa que corresponde ao ID
        pessoa = PessoaDieta.query.filter(PessoaDieta.id_pessoa == idPessoa).first()

        # Se a pessoa foi encontrada, retorna seu dicionário
        return pessoa.to_dict() if pessoa else None
    except SQLAlchemyError as e:
        raise e