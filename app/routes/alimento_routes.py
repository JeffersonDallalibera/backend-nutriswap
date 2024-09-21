# routes/alimentos_routes.py
from app import db
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.models.alimento import Alimento
from app.services.alimentos_service import get_alimentos_by_tipo
from app.services.informacao_nutricional_service import get_informacao_nutricional_by_alimento

alimentos_bp = Blueprint('alimentos', __name__)

@alimentos_bp.route('/alimentos', methods=['GET'])
def list_alimentos():
    tipo_str = request.args.get('tipo')
    if tipo_str:
        try:
            tipo = int(tipo_str)  # Converte o parâmetro para inteiro
            alimentos = get_alimentos_by_tipo(tipo)
            return jsonify([alimento.to_dict() for alimento in alimentos]), 200
        except ValueError:
            return jsonify({'error': 'ID do tipo de alimento inválido'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Tipo de alimento não fornecido'}), 400



@alimentos_bp.route('/calcular-alimento', methods=['POST'])
def calcular_alimento():
    try:
        # Receber dados do JSON enviado pelo frontend
        dados = request.json
        alimento_id = dados.get('alimento_id')
        quantidade = dados.get('quantidade')
        tipo_quantidade = dados.get('tipo_quantidade')  # 'porcao' ou 'quantidade'

        if not alimento_id or not quantidade or not tipo_quantidade:
            return jsonify({'error': 'Dados insuficientes'}), 400

        # Buscar o alimento e suas informações nutricionais no banco de dados
        alimento = Alimento.query.get(alimento_id)
        if not alimento:
            return jsonify({'error': 'Alimento não encontrado'}), 404

        info_nutricional = alimento.informacoes_nutricionais
        if not info_nutricional:
            return jsonify({'error': 'Informações nutricionais não encontradas para o alimento'}), 404

        # Cálculo nutricional
        if tipo_quantidade == 'porcao':
            # Considerar 1 porção = 100g
            quantidade_final = float(quantidade) * 100
        else:
            # Quantidade em gramas diretamente
            quantidade_final = float(quantidade)

        # Calcular os valores nutricionais baseados na quantidade
        calorias = (info_nutricional.calorias / 100) * quantidade_final
        proteinas = (info_nutricional.proteina / 100) * quantidade_final
        carboidratos = (info_nutricional.carboidrato / 100) * quantidade_final
        lipidios = (info_nutricional.lipidio / 100) * quantidade_final
        fibras = (info_nutricional.fibra / 100) * quantidade_final
        vitamina_c = (info_nutricional.vitaminac / 100) * quantidade_final
        calcio = (info_nutricional.calcio / 100) * quantidade_final
        ferro = (info_nutricional.ferro / 100) * quantidade_final
        sodio = (info_nutricional.sodio / 100) * quantidade_final

        resultado = {
            'alimento': alimento.nome,
            'quantidade_gramas': quantidade_final,
            'calorias': calorias,
            'proteinas': proteinas,
            'carboidratos': carboidratos,
            'lipidios': lipidios,
            'fibras': fibras,
            'vitamina_c': vitamina_c,
            'calcio': calcio,
            'ferro': ferro,
            'sodio': sodio
        }

        return jsonify(resultado), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Erro no banco de dados', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro no processamento', 'details': str(e)}), 500