"""Models for project; this is where you create your tables (called classes) and connect to db using flask (a function)"""

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


class Form(db.Model):
    """Dream Disney Day form"""

    __tablename__ = 'form'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    q_travel_grp = db.Column(db.String)
    q_weather = db.Column(db.String)
    q_dark_ride = db.Column(db.Boolean)
    q_thrill_ride = db.Column(db.Boolean)
    q_motion_sick = db.Column(db.Boolean)
    q_foodie = db.Column(db.Boolean)
    q_must_ride = db.Column(db.String)


    user = db.relationship("User", backref="form")
    category = db.relationship("Category", backref="form")

    def __repr__(self):
        return f'<Form form_id={self.id} category_id={self.category_id} user_id={self.user_id}>'


class Category(db.Model):
    """Category that user falls into"""

    __tablename__ = 'category'

    category_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    category_desc = db.Column(db.String)

    #sending category_id to join table via backref

    def __repr__(self):
        return f'<Category category_id={self.category_id}>'


class RideCategory(db.Model):
    """Join table for rides and categories"""

    __tablename__ = 'ridecategory'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    ride_id = db.Column(db.Integer, db.ForeignKey("ride.ride_id"))
    ride_order = db.Column(db.Integer) #Possibly coming in 2.0

    category = db.relationship("Category", backref="ridecategory")
    ride = db.relationship("Ride", backref="ridecategory")

    def __repr__(self):
        return f'<Join join_id={self.id} category_id={self.category_id} ride_order={self.ride_order}>'


class Ride(db.Model):
    """List of rides"""

    __tablename__ = 'ride'

    ride_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    ride_name = db.Column(db.String, unique=True)
    ride_wait_time = db.Column(db.String) #from API

    #sending ride_id to RideCategory table via backref

    def __repr__(self):
        return f'<Ride ride_id={self.id}>'


def connect_to_db(flask_app, db_uri="postgresql:///results", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
