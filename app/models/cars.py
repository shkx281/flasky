from app import db
# from app import migrate

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # driver = db.Column(db.String)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    #driver = db.relationship("Driver", backref="cars")
    # commented out because we are going to backref on the parent
    team = db.Column(db.String)
    mass_kg = db.Column(db.Integer)
    

    def to_dict(self):
        return {
                "id": self.id,
                "driver": self.driver.name,
                "team": self.driver.team,
                "mass_kg": self.mass_kg
            }
    def to_dict_basic(self):
        return {
                "id": self.id,
                "mass_kg": self.mass_kg
        }