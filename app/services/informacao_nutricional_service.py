import pandas as pd
import numpy as np
from app.models.alimento import Alimento
from app.models.informacao_nutricional import InformacaoNutricional
from app.extensions import db
from app.services.similariedade_service import calcular_similaridade


def get_informacao_nutricional_by_alimento(alimento_id):
    try:
        return InformacaoNutricional.query.filter_by(alimento_id=alimento_id).first()
    except Exception as e:
        db.session.rollback()
        raise e


def calcular_informacao_nutricional(info_nutricional, quantidade, tipo_quantidade):
    if tipo_quantidade == 'porcao':
        quantidade_final = float(quantidade) * 100  # 1 porção = 100g
    else:
        quantidade_final = float(quantidade)  # Quantidade em gramas diretamente

    print("calculando informacao nutricional")

    return {
        'calorias': (info_nutricional.calorias / 100) * quantidade_final,
        'proteinas': (info_nutricional.proteina / 100) * quantidade_final,
        'carboidratos': (info_nutricional.carboidrato / 100) * quantidade_final,
        'lipidios': (info_nutricional.lipidio / 100) * quantidade_final,
        'fibras': (info_nutricional.fibra / 100) * quantidade_final,
        'vitamina_c': (info_nutricional.vitaminac / 100) * quantidade_final,
        'calcio': (info_nutricional.calcio / 100) * quantidade_final,
        'ferro': (info_nutricional.ferro / 100) * quantidade_final,
        'sodio': (info_nutricional.sodio / 100) * quantidade_final,
    }


def buscar_equivalente(info_nutricional, tipo, quantidade):
    return calcular_similaridade(info_nutricional, tipo, quantidade)


def adicionar_informacoes_nutricionais(alimento_id, informacoes):
    try:
        nova_informacao_nutricional = InformacaoNutricional(
            alimento_id=alimento_id,
            proteina=informacoes.get('proteina'),
            carboidrato=informacoes.get('carboidrato'),
            lipidio=informacoes.get('lipidio'),
            fibra=informacoes.get('fibra'),
            calorias=informacoes.get('calorias'),
            vitaminac=informacoes.get('vitaminac'),
            calcio=informacoes.get('calcio'),
            ferro=informacoes.get('ferro'),
            sodio=informacoes.get('sodio')
        )

        # Adiciona a informação nutricional ao banco de dados
        db.session.add(nova_informacao_nutricional)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao adicionar informações nutricionais: {str(e)}")
