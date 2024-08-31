# app/jwt_utils.py
import jwt
from datetime import datetime, timedelta
from flask import current_app

def encode_auth_token(user_id):
    """
    Gera um token JWT para o usuário.
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),  # Expira em 1 dia
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    """
    Decodifica o token JWT e retorna o ID do usuário.
    """
    try:
        payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expirado. Por favor, faça login novamente.'
    except jwt.InvalidTokenError:
        return 'Token inválido. Por favor, faça login novamente.'


