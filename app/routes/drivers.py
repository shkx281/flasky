import json
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.drivers import Driver
from app.models.cars import Car

drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")

@drivers_bp.route("", methods=["POST"])
def create_driver():
    request_body = request.get_json()

    new_driver = Driver(
        name=request_body["name"],
        team=request_body["team"],
        country=request_body["country"],
        handsome=request_body["handsome"]
    )

    db.session.add(new_driver)
    db.session.commit()

    return {
        "id": new_driver.id
    }, 201

@drivers_bp.route("", methods=["GET"])
def get_all_drivers():
    response = []
    drivers = Driver.query.all()
    for driver in drivers:
        response.append(
            driver.to_dict()
        )
    return jsonify(response)

def get_one_driver_or_abort(driver_id):
    try:
        driver_id = int(driver_id)
    except ValueError:
        abort(make_response(jsonify({'msg': f"Invalid driver id: '{driver_id}'. ID must be an integer"}), 400))

    chosen_driver = Driver.query.get(driver_id)

    if chosen_driver is None:
        abort(make_response(jsonify({'msg': f'Could not find driver with id {driver_id}'}), 404))
    
    return chosen_driver

@drivers_bp.route("/<driver_id>", methods=["GET"])
def get_one_driver(driver_id):
    
    driver = get_one_driver_or_abort(driver_id)

    return jsonify(driver.to_dict()), 200

def get_car_or_abort(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        abort(make_response(jsonify({'msg': f"Invalid car id: '{car_id}. ID must be an integer"}), 400))

    chosen_car = Car.query.get(car_id) 
    
    if not chosen_car:
        abort(make_response(jsonify({'msg': f"Could not find car with id {car_id}"}), 404))
    return chosen_car

@drivers_bp.route("/<driver_id>/cars", methods=["POST"])
def add_cars_to_driver(driver_id):
    driver = get_one_driver_or_abort(driver_id)

    request_body = request.get_json()
    try:
        car_ids = request_body["car_ids"] # value is a list of ids
    except KeyError:
        return jsonify({'msg': "Missing car_ids in request body"}), 400
        # would this not be a KeyError not ValueError if we don't have a Key??? Review keyerror vs valueerror
        # OMG I WAS RIGHTTTT HAHAAHAHHAHA
    
    if not isinstance(car_ids, list):
        return jsonify({'msg': "Expevted list of car ids"}), 400

    cars = []

    for id in car_ids:
        cars.append(get_car_or_abort(id))
    for car in cars:

        # car.driver_id = driver_id

        # Another way to do nested endpoints... 

        car.driver = driver

        # how does it know to remove the cars from the other keys 
        # because of a foreign key and also cause it is a one to many relationship
        # please rewatch this 

    db.session.commit()

    return jsonify({'msg': "Added cars to driver {driver_id"}), 200


