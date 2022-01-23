"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
# init_app(app)


@app.route("/")
def welcome_page ():
    """Show the Welcome page"""

    return render_template("homepage.html")

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user_exist = crud.get_user_by_email(email)

    if user_exist:
        flash ("This email is already registered on our website. Please log in.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash ("Account created. Please log in.")
    
    return redirect ("/")

@app.route("/login", methods=["POST"])
def log_in():
    """Existing user log in."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user_exist = crud.get_user_by_email(email)
    # check_password = crud.check_user_password(password)

    if user_exist:
        checked_user = crud.check_user_password(email, password)
        if checked_user:
            session['pkey'] = checked_user
            flash ("Success! You are logged in!")
            return redirect("/form")
        else:
            flash ("Wrong password. Please try again.")
    else:
        flash ("No match for email entered. Please create an account.")
    
    return redirect("/")

@app.route("/rides")
def rides_page ():
    """Show the rides page"""

    return render_template("rides.html")  #just for me to look at

@app.route("/form")
def form_page ():
    """Loads form for user"""

    return render_template("form.html")

@app.route("/results")
def results_page ():
    """Shows the results of form"""

    return render_template("results.html")

@app.route("/user_itinerary")
def user_itinerary ():
    """User's first page upon second login"""

    return render_template("user_itinerary.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)