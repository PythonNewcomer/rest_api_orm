from config_reader import ConfigReader
from DataTransformer import DataTransformer
from json import loads
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from country import Country


app = Flask('CountriesREST')
cr = ConfigReader()
host, port, dbname, user, password = cr.get_database_config()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, dbname))
Session = sessionmaker(bind=engine)
session = Session()

db = DataTransformer()


@app.route('/countries', methods=['GET'])
def get_countries():
    result = session.query(Country.id, Country.name, Country.continent).all()
    return db.transform_dataset_into_json(result)


@app.route('/countries/<id>', methods=['GET'])
def get_country(id):
    result = session.query(Country.id, Country.name, Country.continent).filter(Country.id == id)
    return db.transform_row_into_json(result)


@app.route('/countries/<id>', methods=['DELETE'])
def delete_country(id):
    session.query(Country).filter(Country.id == id).delete()
    session.commit()
    message = 'Country {} was deleted!'.format(id)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/countries', methods=['POST'])
def add_country():
    data = loads(request.data)
    name = data['name']
    continent = data['continent']
    country_row = Country(name=name, continent=continent)
    session.add(country_row)
    session.commit()
    message = 'Country {} was added!'.format(name)
    dic = {'message': message}
    return jsonify(dic)


@app.route('/countries', methods=['PUT'])
def update_country():
    data = loads(request.data)
    id = data['id']
    name = data['name']
    continent = data['continent']
    country_row = session.query(Country).filter_by(id = id).first()
    dic = {}
    if country_row is None:
        dic['message'] = 'Country Not Found'
    else:
        country_row.name = name
        country_row.continent = continent
        session.commit()
        dic['message'] = 'Country Was Updated'
    return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)

