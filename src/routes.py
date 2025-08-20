from flask import Flask, request, jsonify, Blueprint
from models import db, User, People, Planet    #hay que importar los modelos que vaya utilizando 

api = Blueprint("api", __name__)


@api.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()   #crear una variable user, ir al model User y hacer una consulta (query) y pedirle todo (all)
    return jsonify([user.serialize() for user in users]), 200           #retorna siempre un jsonify deee.. hacer el for aqui la lista de comprehrension

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not Found"}, 404)
    return jsonify([user.serialize()]), 200

@api.route("/users", methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and password are required"}), 400
    
    new_user = User(
        email=data["email"],
        password=data["password"]
    )

    db.session.add(new_user)
    db.session.commit() 

    return jsonify(new_user.serialize()), 201    


#FAVORITES ROUTES 
#FAVORITES PEOPLE ROUTES / TENGO AGREGAR ELIMINAR Y OBTENER

@api.route("/<int:user_id>/favorites-people/<int:people_id>", methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = db.session.get(User, user_id)
    people = db.session.get(People, people_id)  #tengo que cambiar character por people.

    if not user or not people:
        return jsonify({"msg": "user or people not found"}), 404
    
    if people in user.favorites_people:
        return jsonify({"msg": "character already in favorites"}), 400
    
    user.favorites_people.append(people)

    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorites-people/<int:people_id>", methods=['DELETE'])
def remove_favorites_people(user_id, people_id):
    user = db.session.get(User, user_id)
    people = db.session.get(People, people_id)  #tengo que cambiar character por people.

    if not user or not people:
        return jsonify({"msg": "user or character not found"}), 404
    
    if people in user.favorites_people:
        user.favorites_people.remove(people)
        db.session.commit()

        return jsonify(user.serialize()), 200
    
@api.route("/<int:user_id>/favorites-people", methods=['GET'])
def get_favorites_people(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"msg": "user not found"}), 400
    favorites = [people.serialize() for people in user.favorites_people]
    return jsonify(favorites)
    
    
#FAVORITES PLANETS ROUTES.

@api.route("/<int:user_id>/favorites-planets", methods=['GET'])
def get_favorites_planets(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    favorites = [planet.serialize() for planet in user.favorites_planets]
    return jsonify(favorites)

@api.route("<int:user_id>/favorites-planets/<int:planet_id>", methods=['POST'])
def add_favorites_planets(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    if not user or not planet:
        return jsonify({"msg": "user or planet not found"}), 404
    
    if planet in user.favorites_planets:
        return jsonify({"msg": "planet already exist in favorites"}), 400
    
    user.favorites_planets.append(planet)

    db.session.commit()

    return jsonify(user.serialize()), 201

@api.route("<int:user_id>/favorites-planets/<int:planet_id>", methods=['DELETE'])
def remove_favorites_planets(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet =  db.session.get(Planet, planet_id)

    if not user or not planet:
        return jsonify({"msg": "user or planet not found"}), 404
    
    if planet in user.favorites_planets:
        user.favorites_planets.remove(planet)
        db.session.commit()

        return jsonify(user.serialize()), 201
           