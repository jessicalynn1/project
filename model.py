"""Models for project; this is where you create your tables (called classes) and connect to db using flask (a function)"""

from flask_sqlalchemy import SQLAlchemy
# import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Form(db.Model):
    """Dream Disney Day form"""

    __tablename__ = 'form'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    q_travel_grp = db.Column(db.String)
    q_weather = db.Column(db.String)
    q_dark_ride = db.Column(db.Boolean)
    q_thrill_ride = db.Column(db.Boolean)
    q_motion_sick = db.Column(db.Boolean)
    q_foodie = db.Column(db.Boolean)
    q_must_ride = db.Column(db.String)
    # time_stamp = db.Column(db.datetime)

    user = db.relationship("User", backref="form")
 

    def __repr__(self):
        return f'<Form form_id={self.id} user_id={self.user_id}>'



class FormRide(db.Model):
    """Join table for form and rides"""

    __tablename__ = 'formride'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"))
    ride_id = db.Column(db.Integer, db.ForeignKey("ride.id"))

    form = db.relationship("Form", backref="formride")
    ride = db.relationship("Ride", backref="formride")

    def __repr__(self):
        return f'<FormRide id={self.id} form_id={self.itinerary_id}>'


class Ride(db.Model):
    """List of rides"""

    __tablename__ = 'ride'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    # wait_time = db.Column(db.String) version 2.0


    def __repr__(self):
        return f'<Ride ride_id={self.id} name={self.name}>'


class Itinerary(db.Model):
    """Saved user result"""

    __tablename__ = 'itinerary'

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    formride_id = db.Column(db.Integer, db.ForeignKey("formride.id"), nullable=False)

    formride = db.relationship("FormRide", backref="Itinerary")

    def __repr__(self):
        return f'<Itinerary id={self.id} user_id={self.user_id}>'


def connect_to_db(flask_app, db_uri="postgresql:///results", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import flask_app
    connect_to_db(flask_app)
