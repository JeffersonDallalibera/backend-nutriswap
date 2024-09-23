from flask import Blueprint, jsonify
from app.services.tipo_alimento_service import get_all_tipo_alimento
from app.routes import tipos_alimentos as bp

@bp.route('/tipos_alimento', methods=['GET'])
def list_tipo_alimento():
    try:
        tipos = get_all_tipo_alimento()
        tipo_list = [{'id': tipo.id, 'nome': tipo.nome} for tipo in tipos]
        return jsonify(tipo_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
