# routes/alimentos_routes.py
from flask import Blueprint, request, jsonify
from app.services.alimentos_service import get_alimentos_by_tipo

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
