import pandas as pd
import numpy as np
from app.models.alimento import Alimento
from app.models.informacao_nutricional import InformacaoNutricional
from app.extensions import db


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
    try:
        print('ENTRANDO NO BUSCAR EQUIVALENTE')

        # Converte a quantidade para gramas
        quantidade_gramas = float(quantidade) * 100 if tipo == 'porcao' else float(quantidade)

        # Cálculo dos limites nutricionais
        calorias_target = float(info_nutricional.calorias) * (quantidade_gramas / 100)
        proteina_target = float(info_nutricional.proteina)
        carboidrato_target = float(info_nutricional.carboidrato)
        lipidio_target = float(info_nutricional.lipidio)
        fibra_target = float(info_nutricional.fibra)

        # Buscar o tipo do alimento
        tipoAlimentoId = Alimento.query.filter_by(alimento_id=info_nutricional.alimento_id).first().tipo_alimento_id

        # Buscar todas as informações nutricionais do mesmo tipo
        all_info_nutricional = InformacaoNutricional.query.join(Alimento).filter(
            Alimento.tipo_alimento_id == tipoAlimentoId).all()

        # Criar um DataFrame com as informações
        data = {
            'alimento_id': [],
            'calorias': [],
            'proteina': [],
            'carboidrato': [],
            'lipidio': [],
            'fibra': [],
            # Adicione outros nutrientes aqui
        }

        for info in all_info_nutricional:
            data['alimento_id'].append(info.alimento_id)
            data['calorias'].append(float(info.calorias))
            data['proteina'].append(float(info.proteina))
            data['carboidrato'].append(float(info.carboidrato))
            data['lipidio'].append(float(info.lipidio))
            data['fibra'].append(float(info.fibra))
            # Adicione outros nutrientes aqui

        df = pd.DataFrame(data)

        print(df)

        # Cálculo de similaridade
        df['calorias_diff'] = np.abs(df['calorias'] - calorias_target)
        df['proteina_diff'] = np.abs(df['proteina'] - proteina_target)
        df['carboidrato_diff'] = np.abs(df['carboidrato'] - carboidrato_target)
        df['lipidio_diff'] = np.abs(df['lipidio'] - lipidio_target)
        df['fibra_diff'] = np.abs(df['fibra'] - fibra_target)

        # Calcular uma métrica de similaridade
        df['similaridade'] = df[
            ['calorias_diff', 'proteina_diff', 'carboidrato_diff', 'lipidio_diff', 'fibra_diff']].mean(axis=1)

        # Filtrar os alimentos com base em um critério de similaridade
        equivalentes = df.nsmallest(6, 'similaridade')  # Pegando os 5 mais similares

        # Buscar os objetos Alimento correspondentes e suas informações nutricionais
        alimentos_equivalentes = []
        for alimento_id in equivalentes['alimento_id']:
            # Ignorar o alimento que está sendo procurado
            if alimento_id == info_nutricional.alimento_id:
                continue

            alimento = Alimento.query.filter_by(alimento_id=alimento_id).first()
            info = InformacaoNutricional.query.filter_by(alimento_id=alimento_id).first()
            if alimento and info:
                alimentos_equivalentes.append({
                    'alimento': alimento.to_dict(),
                    'informacao_nutricional': info.to_dict()
                })

        # Retornar a lista de alimentos equivalentes com informações nutricionais
        return alimentos_equivalentes

    except Exception as e:
        db.session.rollback()
        raise e

