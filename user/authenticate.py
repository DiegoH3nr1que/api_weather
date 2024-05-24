import jwt
from .models import UserEntity
from datetime import datetime, timedelta
from django.conf import settings

def authenticate(username, password):
    # regras de autenticação (ignorada por enquanto)
    if username == "user" and password == "a1b2c3":
        #deveria retornar com os dados encontrados no banco
        user = UserEntity(username=username, password=password)
        return user
    return None

def generate_token(user):
    payload = {
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(payload=payload, 
                      key=getattr(settings, "SECRET_KEY"),
                      algorithm='HS256')

def refreshToken(user):
    return generate_token(user)

def verifyToken(token):
    error_code = 0
    payload = None

    try:
        payload = jwt.decode(jwt=token, 
                            key=getattr(settings, "SECRET_KEY"),
                            algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2
    
    return [error_code, payload]


def getAuthenticateUser(token):
    _, payload = verifyToken(token)

    if payload is not None:
        #procurar o usuário no banco
        return UserEntity(username=payload['username'])
