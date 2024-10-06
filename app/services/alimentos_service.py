# services/tipo_alimento_service.py
from app import db
from app.models.alimento import Alimento
from app.services.informacao_nutricional_service import adicionar_informacoes_nutricionais


def get_alimentos_by_tipo(id_tipo_alimento):
    try:
        return Alimento.query.filter_by(tipo_alimento_id=id_tipo_alimento).all()
    except Exception as e:
        db.session.rollback()
        raise e


def criar_alimento(nome, categoria, descricao, tipo_alimento_id, informacoes_nutricionais):
    try:
        # Cria um novo objeto de Alimento
        novo_alimento = Alimento(
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            tipo_alimento_id=tipo_alimento_id
        )

        # Adiciona o novo alimento ao banco de dados
        db.session.add(novo_alimento)
        db.session.flush()  # Necessário para gerar o ID do alimento antes de inserir as informações nutricionais

        # Adiciona as informações nutricionais associadas a este alimento
        adicionar_informacoes_nutricionais(novo_alimento.alimento_id, informacoes_nutricionais)

        db.session.commit()
        return novo_alimento
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao criar alimento: {str(e)}")