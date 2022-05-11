# test_ like how pytest looks for that before 
from app.models.cars import Car

def tests_get_all_cats_with_empty_db_returns_empty_list(client):
    response = client.get('/cars')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_cars_with_populated_db_returns_populated_list(client, seven_cars):
    response = client.get('/cars')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 7

# so do tests not really change the databse itself?
def test_get_one_car_with_populated_db_returns_cars_json(client, seven_cars):
    response = client.get('/cars/1')
    response_body = response.get_json()
    
    # id=1, driver="One", team="Benz", mass_kg=100
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "driver": "One",
        "team": "Benz",
        "mass_kg": 100
    }

def test_post_one_car_creates_car_in_db(client):
    response = client.post('/cars', json = {
        "driver": "Eight", "team": "BMW", "mass_kg": 800})
    response_body = response.get_json()
    assert response.status_code == 201
    assert "id" in response_body
    assert "msg" in response_body

    cars = Car.query.all()
    assert len(cars) == 1
    assert cars[0].driver == "Eight"
    assert cars[0].team == "BMW"
    assert cars[0].mass_kg == 800    

def test_get_one_car_with_empty_db_returns_404(client):
    response = client.get('/cars/1')
    assert response.status_code == 404

def test_get_non_existing_car_with_populated_db_returns_404(client, seven_cars):
    response = client.get('/cars/100')
    assert response.status_code == 404