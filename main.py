from config_reader import ConfigReader
from data_transformer import DataTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movie_tables import Movie, Country, Genre, movies_genres_association
from json import loads
from flask import Flask, jsonify, request, g  # 
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from auth_table import User
from hashlib import md5
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from base import Base


app = Flask('MoviesREST')
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
cr = ConfigReader()
host, port, dbname, user, password = cr.get_database_config()
secret_key = cr.get_secret_key()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, dbname))
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine, checkfirst=True)
db = DataTransformer()


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


@basic_auth.verify_password
def verify_password(username, password):
    hash_password = md5(password.encode('utf-8')).hexdigest()
    stored_password = session.query(User.password_hash).filter_by(username=username).first()[0]
    if hash_password == stored_password:
        g.username = username
        return True
    else:
        return False


@app.route('/token')
@basic_auth.login_required
def get_auth_token():
    token = generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/movies', methods=['GET'])
@token_auth.login_required
def get_movie():
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name, Genre.name) \
        .join(Country, isouter=True) \
        .join(movies_genres_association, isouter=True) \
        .join(Genre, isouter=True) \
        .all()
    return db.transform_dataset_into_json(result)


@app.route('/movies/<id>', methods=['GET'])
@token_auth.login_required
def get_movies(id):
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name, Genre.name) \
        .join(Country, isouter=True) \
        .join(movies_genres_association, isouter=True) \
        .join(Genre, isouter=True) \
        .filter(Movie.id == id)\
        .all()
    return db.transform_row_into_json(result)


@app.route('/movies/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_movie(id):
    session.query(Movie)\
        .filter(Movie.id == id)\
        .delete()
    session.commit()
    message = 'Movie {} was deleted!'.format(id)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/movies', methods=['POST'])
@token_auth.login_required
def add_movie():
    data = loads(request.data)
    title = data['title']
    year = data['year']
    country = data['country']
    genre = data['genre']
    movie_row = Movie(title=title, year=year, country=session.query(Country)
                      .filter(Country.name == country)
                      .first())
    movie_row.genre.append(session.query(Genre).filter(Genre.name == genre)
                           .first())
    session.add(movie_row)
    session.commit()
    message = 'Movie {} was added!'.format(title)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/movies/<id>', methods=['PUT'])
@token_auth.login_required
def update_movie(id):
    data = loads(request.data)
    title = data['title']
    year = data['year']
    country = data['country']
    movie_row = session.query(Movie)\
        .filter_by(id=id)\
        .first()
    dic = {}
    if movie_row is None:
        dic['message'] = 'Movie Not Found'
    else:
        movie_row.title = title
        movie_row.year = year
        movie_row.country = session.query(Country)\
            .filter(Country.name == country)\
            .first()
        session.commit()
        dic['message'] = 'Movie Was Updated'
    return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)

