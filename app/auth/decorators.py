# app/auth/decorators.py
from functools import wraps
from flask import request, jsonify
from app.jwt_utils import decode_auth_token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        user_id = decode_auth_token(token)
        if isinstance(user_id, str):  # Se for uma mensagem de erro
            return jsonify({'error': user_id}), 401
        return f(user_id, *args, **kwargs)
    return decorated_function

