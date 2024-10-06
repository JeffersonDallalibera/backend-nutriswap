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

    print('indo calcular')
    print(nutriente_original)
    print(nutriente_substituto)


    proporcao = nutriente_original / nutriente_substituto
    print(proporcao)
    print(quantidade_original)
    quantidade_ajustada = quantidade_original * proporcao

    return round(quantidade_ajustada,2)

def calcular_similaridade(info_nutricional, tipo, quantidade):
    try:
        print('ENTRANDO NO CÁLCULO DE SIMILARIDADE')

        # Converte a quantidade para gramas
        quantidade_gramas = float(quantidade) * 100 if tipo == 'porcao' else float(quantidade)
        print(f'Quantidade em gramas: {quantidade_gramas}')

        # Cálculo dos limites nutricionais
        calorias_target = float(info_nutricional.calorias) * (quantidade_gramas / 100)
        proteina_target = float(info_nutricional.proteina)
        carboidrato_target = float(info_nutricional.carboidrato)
        lipidio_target = float(info_nutricional.lipidio)
        fibra_target = float(info_nutricional.fibra)

        print('Buscando alimentos equivalentes...')

        # Buscar o tipo do alimento
        tipoAlimentoId = Alimento.query.filter_by(alimento_id=info_nutricional.alimento_id).first().tipo_alimento_id
        print("alimentos encontrados")

        # Buscar todas as informações nutricionais do mesmo tipo
        all_info_nutricional = InformacaoNutricional.query.join(Alimento).filter(
            Alimento.tipo_alimento_id == tipoAlimentoId).all()

        print('Informações nutricionais encontradas')
        data = {
            'alimento_id': [],
            'calorias': [],
            'proteina': [],
            'carboidrato': [],
            'lipidio': [],
            'fibra': [],
        }



        for info in all_info_nutricional:
            print('buscando info')
            print(info.alimento_id)
            print(info.calorias)
            print(info.proteina)
            print(info.carboidrato)
            print(info.lipidio)
            print(info.fibra)
            data['alimento_id'].append(info.alimento_id)
            data['calorias'].append(float(info.calorias))
            data['proteina'].append(float(info.proteina))
            data['carboidrato'].append(float(info.carboidrato))
            data['lipidio'].append(float(info.lipidio))
            data['fibra'].append(float(info.fibra))

        df = pd.DataFrame(data)
        df['calorias_diff'] = np.abs(df['calorias'] - calorias_target)
        df['proteina_diff'] = np.abs(df['proteina'] - proteina_target)
        df['carboidrato_diff'] = np.abs(df['carboidrato'] - carboidrato_target)
        df['lipidio_diff'] = np.abs(df['lipidio'] - lipidio_target)
        df['fibra_diff'] = np.abs(df['fibra'] - fibra_target)

        df['similaridade'] = df[
            ['calorias_diff', 'proteina_diff', 'carboidrato_diff', 'lipidio_diff', 'fibra_diff']].mean(axis=1)

        equivalentes = df.nsmallest(6, 'similaridade')  # Pegando os 5 mais similares

        alimentos_equivalentes = []
        print('entrando no for...')
        for alimento_id in equivalentes['alimento_id']:
            if alimento_id == info_nutricional.alimento_id:
                continue

            alimento = Alimento.query.filter_by(alimento_id=alimento_id).first()
            info = InformacaoNutricional.query.filter_by(alimento_id=alimento_id).first()
            if alimento and info:
                print('buscando quantidade')
                # Ajusta a quantidade do alimento substituto
                quantidade_ajustada = ajustar_quantidade_equivalente(info_nutricional, info, quantidade_gramas)

                alimentos_equivalentes.append({
                    'alimento': alimento.to_dict(),
                    'informacao_nutricional': info.to_dict(),
                    'quantidade_ajustada': quantidade_ajustada
                })

        return alimentos_equivalentes

    except Exception as e:
        db.session.rollback()
        raise e
