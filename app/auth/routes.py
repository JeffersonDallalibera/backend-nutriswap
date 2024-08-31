# app/auth/routes.py
from flask import request, jsonify, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.models.usuarios import Usuario
from app.jwt_utils import encode_auth_token, decode_auth_token
from app.auth.decorators import token_required


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("fazendo o login com os dados: ", data)
    username = data.get('username')
    password = data.get('password')

    user = Usuario.query.filter_by(username=username).first()
    if user and user.check_password(password):
        print('Login successful')
        print(user)
        token = encode_auth_token(user.user_id)
        print("token: " + token)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'error': 'Usuário ou senha inválidos'}), 401


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # Aqui você pode invalidar o token se estiver armazenando tokens em algum lugar, caso contrário, apenas retorne uma mensagem
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@bp.route('/check_auth', methods=['GET'])
def check_auth():
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user_id = decode_auth_token(auth_token)
        if isinstance(user_id, str):  # Se for uma mensagem de erro
            return jsonify({'error': user_id}), 401
        return jsonify({'message': 'Token válido', 'user_id': user_id}), 200
    return jsonify({'error': 'Token não fornecido'}), 401


@bp.route('/protected', methods=['GET'])
@token_required
def protected_route(user_id):
    # Acesso concedido
    return jsonify({'message': 'Acesso concedido', 'user_id': user_id}), 200

