from data_transformer import DataTransformer
from movie_tables import Movie, Country, Genre, movies_genres_association
from json import loads
from flask import Flask, jsonify, request
from base import session
from auth_provider import token_auth, basic_auth, generate_auth_token


app = Flask('MoviesREST')

db = DataTransformer()


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

