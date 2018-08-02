from config_reader import ConfigReader
from data_transformer import DataTransformer
from json import loads
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movie_tables import Movie, Country, Genre, movies_genres_association


app = Flask('MoviesREST')
cr = ConfigReader()
host, port, dbname, user, password = cr.get_database_config()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, dbname))
Session = sessionmaker(bind=engine)
session = Session()

db = DataTransformer()


@app.route('/movies', methods=['GET'])
def get_movie():
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name, Genre.name).join(Country)\
        .join(movies_genres_association).join(Genre).all()
    return db.transform_dataset_into_json(result)


@app.route('/movies/<id>', methods=['GET'])
def get_movies(id):
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name, Genre.name).join(Country)\
        .join(movies_genres_association).join(Genre).filter(Movie.id == id).all()
    return db.transform_row_into_json(result)


@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    session.query(Movie).filter(Movie.id == id).delete()
    session.commit()
    message = 'Movie {} was deleted!'.format(id)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/movies', methods=['POST'])
def add_movie():
    data = loads(request.data)
    title = data['title']
    year = data['year']
    country = data['country']
    genre = data['genre']
    movie_row = Movie(title=title, year=year, country=session.query(Country).filter(Country.name == country).first())
    movie_row.genre.append(session.query(Genre).filter(Genre.name == genre).first())
    session.add(movie_row)
    session.commit()
    message = 'Movie {} was added!'.format(title)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    data = loads(request.data)
    title = data['title']
    year = data['year']
    country = data['country']
    movie_row = session.query(Movie).filter_by(id=id).first()
    dic = {}
    if movie_row is None:
        dic['message'] = 'Movie Not Found'
    else:
        movie_row.title = title
        movie_row.year = year
        movie_row.country = session.query(Country).filter(Country.name == country).first()
        session.commit()
        dic['message'] = 'Movie Was Updated'
    return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)

