"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, Form, FormRide, User, Ride, Category, RideCategory
import crud

from jinja2 import StrictUndefined
import webbrowser
import requests
import json 
from pprint import pprint
import bcrypt

app = Flask(__name__, static_url_path='/static') 
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def welcome_page():
    """Show the Welcome page"""

    return render_template("homepage.html")

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    if email == "" or password == "":
        flash ("Not a valid email/password combination.")
    else:
        user_exist = crud.get_user_by_email(email)

        if user_exist:
            flash ("This email is already registered on our website. Please log in.")
        else:
            user = crud.create_user(email, password)
            db.session.add(user)
            db.session.commit()
            flash ("Account created! Please log in.")
    
    return redirect ("/")

@app.route("/login", methods=["POST"])
def log_in():
    """Existing user log in."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    
    user = crud.get_user_by_email(email)
    # user_profile = session.get("results", {})
    
    if not user or user.password != password:
        flash("Your input does not match our records. Please try again.")

    else:
        session["pkey"] = user.user_id
        flash(f"Welcome back, {user.email}!")
        return redirect("/user_homepage")
   
    return redirect("/")

@app.route("/logout")
def logout():
    """User must be logged in."""
    
    if "pkey" in session:
        del session["pkey"]
        flash("Logged Out.")
    return redirect("/")


@app.route("/rides")
def rides_page():
    """Show the rides page"""

    res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
    response = res.json()
    pprint(response)

    return render_template("rides.html", rides=response)


@app.route("/user_homepage")
def user_homepage():
    """Asks if you want a new itinerary or see saved."""

    form = Form.query.filter_by(user_id=session['pkey']).order_by(Form.id.desc()).first()

    return render_template("user_homepage.html", form=form)


@app.route("/filter-ride", methods=["POST"])
def _filter_rides():
    """Private endpoint to create an association object between rides and a category"""
    
    rides = request.form.getlist("ride")
    category = request.form.get("category")
    
    for ride in rides:
        db_ride = crud.get_ride_by_name(ride)
        db_category = crud.get_category_by_name(category)
        db_paired = RideCategory.query.filter_by(ride_id=db_ride.id, category_id=db_category.id).first()
        if not db_paired:
            obj = RideCategory(ride_id=db_ride.id, category_id=db_category.id)
            db.session.add(obj)
            db.session.commit()
            
    return redirect("/ride_filter")

@app.route("/form")
def form_page():
    """Loads form for user"""

    return render_template("form.html")


@app.route("/results", methods=['POST'])
def results_page():
    """Shows the results of form"""

    trip_name = request.form.getlist("trip-name")
    a_travel_grp = request.form.get("q_travel_grp")
    a_weather = request.form.get("q_weather")
    if request.form.get("q_dark_ride") == "True":
        a_dark_ride = True
    else:
        a_dark_ride = False
    
    if request.form.get("q_thrill_ride") == "True":
        a_thrill_ride = True
    else:
        a_thrill_ride = False

    a_motion_sick = request.form.get("q_motion_sick")

    if request.form.get("q_motion_sick") == "True":
        a_motion_sick = True
    else:
        a_motion_sick = False

    if request.form.get("q_foodie") == "True":
        a_foodie = True
    else:
        a_foodie = False

    must_ride_1 = request.form.get("must_ride_1")
    must_ride_2 = request.form.get("must_ride_2")
    must_ride_3 = request.form.get("must_ride_3")

    itinerary_set = set()

# could write a function for these below
# query on ridecategory join on category and filter by category id

    if a_travel_grp == 'Adults; no kids':
        c_id = crud.get_category_by_name('Adults').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)
    
    if a_travel_grp == 'Family; kids under 8':
        c_id = crud.get_category_by_name('Kid').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_travel_grp == 'Family; kids over 8':
        c_id = crud.get_category_by_name('Thrill').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)
    
    if a_travel_grp == 'Large group, 6+':
        c_id = crud.get_category_by_name('Large Group').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_weather == 'hot':
        c_id = crud.get_category_by_name('Water').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_dark_ride:
        c_id = crud.get_category_by_name('Dark').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_thrill_ride:
        c_id = crud.get_category_by_name('Thrill').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if not a_motion_sick:
        c_id = crud.get_category_by_name('Motion').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_foodie:
        c_id = crud.get_category_by_name('Foodie').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)


    new_profile = Form(user_id=session['pkey'], q_travel_grp=a_travel_grp, q_weather=a_weather, q_dark_ride=a_dark_ride,
                        q_thrill_ride=a_thrill_ride, q_motion_sick=a_motion_sick, q_foodie=a_foodie, q_must_ride_1=must_ride_1,
                        q_must_ride_2=must_ride_2, q_must_ride_3=must_ride_3)   #need to add datetime??    
    db.session.add(new_profile)
    db.session.commit()

    form_id = new_profile.id

    itinerary_dict = {}

    for ride_obj in itinerary_set:
        itinerary_dict[ride_obj.ride_id] = ride_obj

    for ride_obj in itinerary_dict.values():
        saved_result = FormRide(form_id=form_id, ride_id=ride_obj.ride_id)
        db.session.add(saved_result)
        db.session.commit()


    results_dict = {}

    for ride_obj in itinerary_set:
        if ride_obj.category.name not in results_dict:
            results_dict[ride_obj.category.name] = [ride_obj.ride.name]
        else:
            results_dict[ride_obj.category.name].append(ride_obj.ride.name)


    return render_template("results.html", results_dict=results_dict, trip_name=trip_name, 
                    must_ride_1=must_ride_1, must_ride_2=must_ride_2, must_ride_3=must_ride_3,)

    # figure out how to email the result to the user in 2.0


@app.route("/ride_filter")
def ride_filter():
    """Put rides into category"""

    rides = Ride.query.all()
    categories = Category.query.all()

    return render_template("ride_filter.html", rides=rides, categories=categories)


@app.route("/user_profile")
def user_profile():
    """User's first page upon second login"""

    form = Form.query.filter_by(user_id=session['pkey']).order_by(Form.id.desc()).first()
    saved_result = FormRide.query.filter_by(form_id=form.id).all()
    print(form)

    ride_dict = {}

    for ride_obj in saved_result:
        ride = ride_obj.ride
        ride_id = ride.id
        ride_categories = RideCategory.query.filter_by(ride_id=ride_id).all()

        for rc in ride_categories:
            if rc.category.name == 'Water' and form.q_weather != "hot":
                continue
            if rc.category.name == 'Adults' and form.q_travel_grp != "Adults; no kids":
                continue
            if rc.category.name == 'Kid' and form.q_travel_grp != "Family; kids under 8":
                continue
            if rc.category.name == 'Large Group' and form.q_travel_grp != "Large group, 6+":
                continue
            if rc.category.name == 'Thrill' and not form.q_thrill_ride:
                continue
            if rc.category.name == 'Dark' and not form.q_dark_ride:
                continue
            if rc.category.name == 'Motion' and form.q_motion_sick:
                continue
            if rc.category.name == 'Foodie' and not form.q_foodie:
                continue
            rc_name = rc.category.name
            if rc_name not in ride_dict:
                ride_dict[rc_name] = [ride.name]
            else:
                ride_dict[rc_name].append(ride.name)       

    return render_template("user_profile.html", ride_dict=ride_dict) 



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)