"""create, read, update, delete; import from model your db; this is where you define functions, access the html, and return data"""

from model import db, User, Form, Category, Join, Ride, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users_list():
    """Shows list of all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user object by its ID"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Check if user with email exists.
        If true, return user. 
        If false, return None."""
    
    return User.query.filter_by(email = email).first()

def check_user_password(email, password):
    """If password entered matches password in databse, return True.
        If password does not  match, return False."""
    
    user = User.query.filter(User.email == email).first()

    if user.password == password:
        return user.user_id
    else:
        return None
        
def all_forms_by_user(user_id):
    """Shows all itineraries of one user."""

    return Form.query.filter(Form.user_id == user_id).all()

def get_result(category_id):
    """Show dream day result"""

    return Category.query.filter(Category.category_id == category_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)