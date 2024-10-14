import numpy as np
import pandas as pd
from app.models.alimento import Alimento
from app.models.informacao_nutricional import InformacaoNutricional
from app import db

def ajustar_quantidade_equivalente(info_original, info_substituto, quantidade_original, nutriente='carboidrato'):
    # Pegando o valor do nutriente-chave (pode ser carboidrato, proteína, etc.)
    nutriente_original = float(getattr(info_original, nutriente))
    nutriente_substituto = float(getattr(info_substituto, nutriente))


    # Calculando a proporção para ajustar a quantidade do substituto
    if nutriente_substituto == 0:
        return quantidade_original  # Evita divisão por zero, mantendo a quantidade original


    proporcao = nutriente_original / nutriente_substituto
    quantidade_ajustada = quantidade_original * proporcao

    return round(quantidade_ajustada,2)


def calcular_similaridade(info_nutricional, tipo, quantidade):
    try:
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

        data = {
            'alimento_id': [],
            'calorias': [],
            'proteina': [],
            'carboidrato': [],
            'lipidio': [],
            'fibra': [],
        }

        for info in all_info_nutricional:
            data['alimento_id'].append(info.alimento_id)
            data['calorias'].append(float(info.calorias))
            data['proteina'].append(float(info.proteina))
            data['carboidrato'].append(float(info.carboidrato))
            data['lipidio'].append(float(info.lipidio))
            data['fibra'].append(float(info.fibra))

        df = pd.DataFrame(data)

        # Cálculo das diferenças
        df['calorias_diff'] = np.abs(df['calorias'] - calorias_target)
        df['proteina_diff'] = np.abs(df['proteina'] - proteina_target)
        df['carboidrato_diff'] = np.abs(df['carboidrato'] - carboidrato_target)
        df['lipidio_diff'] = np.abs(df['lipidio'] - lipidio_target)
        df['fibra_diff'] = np.abs(df['fibra'] - fibra_target)

        # Cálculo da similaridade
        df['similaridade'] = df[
            ['calorias_diff', 'proteina_diff', 'carboidrato_diff', 'lipidio_diff', 'fibra_diff']].mean(axis=1)

        # Evitar divisão por zero e calcular a similaridade percentual
        max_diffs = df[['calorias_diff', 'proteina_diff', 'carboidrato_diff', 'lipidio_diff', 'fibra_diff']].max()

        # Verifica se os valores máximos não são zero
        if (max_diffs == 0).all():
            df['similaridade_percentual'] = 100  # Se todas as diferenças são zero, a similaridade é máxima
        else:
            df['similaridade_percentual'] = 100 - (df['similaridade'] / max_diffs.max() * 100)

        # Verifica se houve algum cálculo válido
        df['similaridade_percentual'] = df['similaridade_percentual'].fillna(0)  # Preenche NaN com 0

        # Pegando os 5 mais similares
        equivalentes = df.nsmallest(6, 'similaridade')

        alimentos_equivalentes = []
        for alimento_id in equivalentes['alimento_id']:
            if alimento_id == info_nutricional.alimento_id:
                continue

            alimento = Alimento.query.filter_by(alimento_id=alimento_id).first()
            info = InformacaoNutricional.query.filter_by(alimento_id=alimento_id).first()
            if alimento and info:
                # Ajusta a quantidade do alimento substituto
                quantidade_ajustada = ajustar_quantidade_equivalente(info_nutricional, info, quantidade_gramas)

                # Adiciona o grau de similaridade
                grau_similaridade = df.loc[df['alimento_id'] == alimento_id, 'similaridade_percentual']
                if not grau_similaridade.empty:
                    grau_similaridade = grau_similaridade.iloc[0]  # Pega o valor escalar

                alimentos_equivalentes.append({
                    'alimento': alimento.to_dict(),
                    'informacao_nutricional': info.to_dict(),
                    'quantidade_ajustada': quantidade_ajustada,
                    'grau_similaridade': round(grau_similaridade, 2)  # Inclui o grau de similaridade
                })

        return alimentos_equivalentes

    except Exception as e:
        db.session.rollback()
        raise e

