from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.cars import Car

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

@cars_bp.route("", methods=["POST"])
def create_car():
    request_body=request.get_json()

    new_car = Car(
        driver=request_body["driver"],
        team=request_body["team"],
        mass_kg=request_body["mass_kg"]
    )

    db.session.add(new_car)
    db.session.commit()

    return {
        "id": new_car.id,
        "msg": f"Successfully created a car with id: '{new_car.id}'"
    }, 201

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    # queryparams... always optional, not a required part of an endpoint
    # I could add a bunch of query params
    # what is I want the request to be case insensitive.. can I do .lower()? 
    # what is I want to make the table vals also case insensitive
    params = request.args
    
    # or params = request.args.get("team_name") with only one param key without the function call --> ()
    # if "team" in params and "driver" in params:
    #     # check otters hithub
    if "team" in params:
        team_name = params["team"]
        cars = Car.query.filter_by(team=team_name)
        # .filter_by versus query.filter
    elif "kg_int" in params:
        kg_int = params["kg_int"]
        cars = Car.query.filter_by(mass_kg=kg_int)
    else:
        cars = Car.query.all()
    response = []
    for car in cars:
        response.append(
            {
                "id": car.id,
                "driver": car.driver,
                "team": car.team,
                "mass_kg": car.mass_kg
            }
        )
    return jsonify(response)
    # what if the table is empty?

@cars_bp.route("<car_id>", methods=["GET"])
def get_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({"msg": "must return int"}), 400
    
    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404
    
    return jsonify({
        "id": chosen_car.id,
        "driver": chosen_car.driver,
        "team": chosen_car.team,
        "mass_kg": chosen_car.mass_kg
    })

@cars_bp.route("/<car_id>", methods=["PUT"]) #what if you need to just patch the driver or mass_kg
# and want to do it without rewriting everything
# Jasmine also added PATCH since it should be the same.
def replace_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({"msg": f"Invalid car id: '{car_id}'. ID must be an integer"}), 400

    request_body = request.get_json()
    
    # I did len of request_body for the below portion, would that not be a good practice
    # if not driver in   VS if driver not in??
    if "driver" not in request_body or \
        "team" not in request_body or\
        "mass_kg" not in request_body:
        return jsonify({"msg": f"Request must include driver, team, and mass_kg"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404

    chosen_car.driver = request_body["driver"]
    chosen_car.team = request_body["team"]
    chosen_car.mass_kg = request_body["mass_kg"]

    db.session.commit()

    # is this... returning a msg... always necessary? or just good HTTP practice?
    # is msg a standard ?? can flask recognize msg??
    return jsonify({"msg": f"Successfully replaced car with id {car_id}"})

    # make_response is a function from the flask module VS jsonfiy??

@cars_bp.route("<car_id>", methods=["DELETE"])
def delete_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({"msg": f"Invalid car id: '{car_id}'. ID must be an integer"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404

    db.session.delete(chosen_car)
    db.session.commit()

    return jsonify({"msg": f"Deleted car with id {car_id}"}) # no status code cuz 200 should be good enough

def get_car_or_abort(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        rsp = {"msg": f"invalid id: {car_id}"}
        abort(make_response(jsonify(rsp),400))
    
    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404











#------------------------------------------------------------------

# class Car:
#     def __init__(self, id, driver, team, mass_kg):
#         self.id = id
#         self.driver = driver
#         self.team = team
#         self.mass_kg = mass_kg
    
# cars  = [
#     Car(7, "Sainz", "ferarri", 795),
#     Car(88, "Sharles", "Ferrari", 800),
#     Car(4, "Danny Ric", "McLaren", 1138)
# ]

# cars_bp = Blueprint("cars", __name__, url_prefix="/cars")
# could do url_prefix="/cars" so then the .route('') \
# will be empty. We could add but changes what the route is.
# I changed it today 4/26. Took out .route('/cars') and added url_prefix
# REWATCHHH 

# @cars_bp.route('', methods=["GET"]) # let's us know that this function needs to handle a route
# def get_all_cars():
#     response = []
#     for car in cars:
#         response.append(
#             {
#             "id": car.id,
#             "driver": car.driver,
#             "team": car.team,
#             "mass_kg": car.mass_kg
#         }
#         )
#     return jsonify(response)

# @cars_bp.route('/<car_id>', methods=["GET"])
# def get_one_car(car_id):
#     try:
#         car_id = int(car_id)
#     except ValueError:
#         return jsonify({'msg': f"Invalid car id: '{car_id}' ID must be an integer"}), 400
#         # outsides "   ' ' " is prettier than '  " "  '
#         # single quotes do not need to be escaoed \. 
#     chosen_car = None
#     for car in cars:
#         if car.id == car_id:
#             chosen_car =({
#                 'id': car.id,
#                 'driver': car.driver,
#                 'team': car.team,
#                 'mass_kg': car.mass_kg
#             })    
#     if chosen_car is None:
#     #     message = 'No car found'
#     #     return message, 404
#     # return jsonify(chosen_car)
#         return jsonify({'msg': f'Could not find car with id {car_id}'}), 404 
    
#     return jsonify(chosen_car)

# very typical to have ids as ints.
# Json equivalent of None is null.

# If using a helper function, you can use abort. 

