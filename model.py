"""Models for project; this is where you create your tables (called classes) and connect to db using flask (a function)"""

import datetime
from flask_sqlalchemy import SQLAlchemy

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
    
    
class Ride(db.Model):
    """List of rides"""

    __tablename__ = 'rides'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)    
    # wait_time = db.Column(db.String) version 2.0

    def __repr__(self):
        return f'<Ride id={self.id} name={self.name}>'


class Category(db.Model):
    """List of ride categories"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    
    def __repr__(self):
        return f'<Category id={self.id} name={self.name}>'
    

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
    q_must_ride_1 = db.Column(db.String)
    q_must_ride_2 = db.Column(db.String)
    q_must_ride_3 = db.Column(db.String)
    # time_created = db.column(db.DateTime(timezone=True))

    user = db.relationship("User", backref="form")

    def __repr__(self):
        return f'<Form form_id={self.id} user_id={self.user_id}>'


class FormRide(db.Model):
    """Join table for form and rides"""

    __tablename__ = 'formride'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey("rides.id"), nullable=False)

    form = db.relationship("Form", backref="formride")
    ride = db.relationship("Ride", backref="formride")

    def __repr__(self):
        return f'<FormRide id={self.id} form_id={self.form_id} ride_id={self.ride_id} '


class RideCategory(db.Model):
    """Association table for rides and their categories"""
    __tablename__ = 'ride_categories'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey("rides.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    
    ride = db.relationship("Ride", backref="ride_categories")
    category = db.relationship("Category", backref="ride_categories")

    def __repr__(self):
        return f'<RideCategory id={self.id} ride_id={self.ride_id} category_id={self.category_id}>'


def example_data():
    """Create some sample data."""

    Category.query.delete()
    Ride.query.delete()

    adults = Category(name="Adults")
    thrill = Category(name="Thrill")
    kid = Category(name="Kid")

    user = User(email="quorra@hotmail.com", password="1234")

    hm = Ride(name="Haunted Mansion")
    mb = Ride(name="Matterhorn Bobsleds")
    mtp = Ride(name="Mad Tea Party")

    db.session.add_all([adults, thrill, kid, hm, mb, mtp, user])
    db.session.commit()

def connect_to_db(app, db_uri="postgresql:///results", echo=False):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = echo
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
