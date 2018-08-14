from auth_table import User
from hashlib import md5
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from config_reader import ConfigReader
from base import session

token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()
cr = ConfigReader()
secret_key = cr.get_secret_key()


@basic_auth.verify_password
def verify_password(username, password):
    hash_password = md5(password.encode('utf-8')).hexdigest()
    stored_password = session.query(User.password_hash).filter_by(username=username).first()[0]
    if hash_password == stored_password:
        g.username = username
        return True
    else:
        return False


def generate_auth_token(expiration=600):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({'user': g.username})


@token_auth.verify_token
def verify_auth_token(token):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    if session.query(User.username).filter_by(username=data['user']).first()[0]:
        return True
    else:
        return False


