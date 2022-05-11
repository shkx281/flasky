# must be named like so. HAS to be next to app file.
import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cars import Car

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
# when we do flask run this is usually done for us.. but we're manually doing this.

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seven_cars(app):
    car1 = Car(id=1, driver="One", team="Benz", mass_kg=100)
    car2 = Car(id=2, driver="Two", team="Benzz", mass_kg=100)
    car3 = Car(id=3, driver="Three", team="Benzzz", mass_kg=300)
    car4 = Car(id=4, driver="Four", team="Benzzzz", mass_kg=400)
    car5 = Car(id=5, driver="Five", team="Benzzzzz", mass_kg=500)
    car6 = Car(id=6, driver="Six", team="Benzzzzzz", mass_kg=100)
    car7 = Car(id=7, driver="Seven", team="Benzzzzzzz", mass_kg=700)
    # you don't have to add the id b/c we have the autoincrement, \
    # but I want to know exactly what my database is. We can ssign if the id is not taken.

    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.add(car5)
    db.session.add(car6)
    db.session.add(car7)

    db.session.commit()
