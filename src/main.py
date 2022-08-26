"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, FavPeople, Planets, FavPlanets

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def getPeople():
    all_people = People.query.all()
    serializados = list(map(lambda people:people.serialize(), all_people))
    print(all_people)
    return jsonify({
        "mensaje": "Todas las personas",
        "people": serializados
        }), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def getOnePeople(people_id):
    one_people = People.query.filter_by(uid=people_id).first()
    print(one_people)
    if(one_people):
        return jsonify({
            "ID": people_id,
            "People":one_people.serialize()
        }), 200
    else:
        return jsonify({
            "People Id buscado" : people_id,
            "Mensaje": "People no encontrado"
        })

@app.route('/planets', methods=['GET'])
def getPlanets():
    all_planets = Planets.query.all()
    serializados2 = list(map(lambda planets:planets.serialize(), all_planets))
    return jsonify({
        "mensaje": "Todos los planetas",
        "people": serializados2
        }), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def getOnePlanets(planets_id):
    one_planet = Planets.query.filter_by(uid=planets_id).first()
    print(one_planet)
    if(one_planet):
        return jsonify({
            "ID": planets_id,
            "Planet":one_planet.serialize()
        }), 200
    else:
        return jsonify({
            "Planet Id buscado" : planets_id,
            "Mensaje": "Planet no encontrado"
        })

@app.route('/user', methods=['GET'])
def handle_hello():
    all_user = User.query.all()
    all_user_serializado = list(map(lambda user:user.serialize(), all_user))
    #guarda en all_user... lista de info serializada de los usuarios 
    #La serialización tambien se realizó en Models.py
    print(all_user)
    return jsonify({
        "mensaje" : "todos los usuarios",
        "user" : all_user_serializado
        })

@app.route('/user/favorites', methods=['GET'])
def userfav():
    userfav = FavPeople.query.all() 
    #Consulta todos los favoritos de la class Favpeople de models.py
    userfav_serializado = list(map(lambda favpeople:favpeople.serialize(), userfav))
    print(userfav)
    return jsonify({
        "mensaje" : "todos los favoritos",
        "user" : userfav_serializado
        })

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
#El POST se debe hacer enviando llaves "email": "email ingresado ya en user"
def postPeopleFav(people_id):
    body = request.get_json()
    newFav = FavPeople(user=body['email'], people = people_id)
    db.session.add(newFav)
    db.session.commit()
    return "nuevo personaje favorito agregado"

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
# el post se debe hacer enviando entre llaves "email": "xx"
def postPlanetFav(planet_id):
    body = request.get_json()
    #Recibe la informacion en formato JSON"
    newFavP = FavPlanets(user=body['email'], planet = planet_id)
    #Busca en class FavPlanets coincidencia de usuario y planeta id
    db.session.add(newFavP)
    db.session.commit()
    #Incorpora en base de datos SQLAlchemy
    return "nuevo planeta favorito agregado"

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def DeletePeopleFav(people_id):
    people_delete = FavPeople.query.get(people_id)
    #people_eliminar = FavPeople.query.filter_by(id=people_id).first()
    db.session.delete(people_delete)
    db.session.commit()
    return "People eliminado"

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def DeletePlanetFav(planet_id):
    planet_delete = FavPlanets.query.filter_by(id=planet_id).first()
    """#planet_delete = FavPlanets.query.get(planet_id)"""
    db.session.delete(planet_delete)
    db.session.commit()
    return "planet_id eliminado"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
