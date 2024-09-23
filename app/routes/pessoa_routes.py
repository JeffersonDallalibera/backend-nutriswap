from flask import Blueprint, request, jsonify
from app.services.pessoa_service import inserir_pessoa, buscar_todas_pessoas
from app.routes import pessoa as bp

@bp.route('/pessoa', methods=['GET'])
def obter_pessoas():
    try:
        pessoas = buscar_todas_pessoas()
        return jsonify(pessoas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/pessoa/adicionar', methods=['POST'])
def adicionar_pessoa():
    try:
        pessoa_data = request.get_json()
        print(pessoa_data)
        nova_pessoa = inserir_pessoa(pessoa_data)
        return jsonify(nova_pessoa), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
