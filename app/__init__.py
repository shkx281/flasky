from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() # function call.

def create_app(testing=None): # a function that runs everytime flask starts
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if not testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('TESTING_SQLALCHEMY_DATABASE_URI')

    # if testing == {'testing':True}:
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('TESTING_SQLALCHEMY_DATABASE_URI')

    # else:
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')


    # we're going to pull this file into an env file. Benefit is it's easier to change
    # environmental variables
    # allows app to be more flexible


    db.init_app(app)
    # initializes the app. hooking up our application
    migrate.init_app(app, db)
    # take this db and migrate object and connect them to this flask server
    
    from .models.cars import Car
    from .models.drivers import Driver

    from .routes.cars import cars_bp # going and getting bp
    app.register_blueprint(cars_bp) # telling our app about this blueprint

    return app # flask able to get app back