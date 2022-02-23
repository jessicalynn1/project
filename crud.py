"""create, read, update, delete; import from model your db; this is where you define functions, access the html, and return data"""

from model import db, User, Form, connect_to_db, Ride, FormRide, RideCategory, Category

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users_list():
    """Shows list of all users."""

    return User.query.all()

def get_user_by_id(id):
    """Return a user object by its ID"""
    return User.query.get(id)

def get_user_by_email(email):
    """Check if user with email exists.
        If true, return user. 
        If false, return None."""
    
    return User.query.filter_by(email=email).first()

def check_user_password(email, password):
    """If password entered matches password in database, return True.
        If password does not  match, return False."""
    
    user = User.query.filter_by(email=email, password=password).first()

    if user.password == password:
        return user.user_id
    else:
        return None
        
def all_forms_by_user(user_id):
    """Shows all itineraries of one user."""

    return Form.query.filter(Form.user_id == user_id).all()

def save_result(id, form_id, ride_id):
    """Show dream day result"""
    
    id = FormRide(id=id)
    form_id = FormRide(form_id=form_id)
    ride_id = FormRide(ride_id=ride_id)
    
    result = FormRide(id=id, form_id=form_id, ride_id=ride_id)

    return result

def print_result(id):     # , form_id, ride_id)
    """Print dream day result on user profile page"""

    # id = FormRide(id=id)
    # form_id = FormRide(form_id=form_id)
    # ride_id = Ride(ride_id=id)
    # ride_name = Ride(name=ride_id)
    
    # result = FormRide(id=id, form_id=form_id, ride_id=ride_name)

    return FormRide.query.filter_by(id=id).all()

def create_ride(name):
    """Create and return a ride."""
    
    ride = Ride(name=name)
    
    return ride

def get_ride_by_name(name):
    """Query a ride by its name"""

    return Ride.query.filter_by(name=name).first()

def get_category_by_name(name):
    """Query a category by its name"""

    return Category.query.filter_by(name=name).first()

def create_ride_category(ride_id, category_id):
    """Creates an object between a ride and its category"""

    ride = RideCategory(ride_id=ride_id, category_id=category_id)
    db.session.add(ride)
    db.session.commit()
    return ride

if __name__ == '__main__':
    from server import app
    connect_to_db(app)