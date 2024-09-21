# routes/nutricao_routes.py
from app import db
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.services.informacao_nutricional_service import (
    get_informacao_nutricional_by_alimento,
    buscar_equivalente
)

nutricao_bp = Blueprint('nutricao', __name__)

@nutricao_bp.route('/busca-equivalente', methods=['POST'])
def busca_equivalente_route():
    try:
        dados = request.json
        alimento_id = dados.get('alimento_id')
        tipo = dados.get('tipo_quantidade')  # Pode ser usado para filtrar equivalentes
        quantidade = dados.get('quantidade')

        print(alimento_id, tipo, quantidade)

        if not alimento_id or not quantidade or tipo is None:
            return jsonify({'error': 'Dados insuficientes'}), 400

        # Buscar as informações nutricionais do alimento
        info_nutricional = get_informacao_nutricional_by_alimento(alimento_id)

        if not info_nutricional:
            return jsonify({'error': 'Informações nutricionais não encontradas para o alimento'}), 404

        # Buscar alimentos equivalentes
        equivalentes = buscar_equivalente(info_nutricional, tipo, quantidade)

        return jsonify({
            'alimento_id': alimento_id,
            'tipo': tipo,
            'quantidade': quantidade,
            'informacao_nutricional': {
                'calorias': info_nutricional.calorias,
                'proteina': info_nutricional.proteina,
                'carboidrato': info_nutricional.carboidrato,
                'lipidio': info_nutricional.lipidio,
                'fibra': info_nutricional.fibra,
            },
            'equivalentes': equivalentes
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Erro no banco de dados', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro no processamento', 'details': str(e)}), 500

