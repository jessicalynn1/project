"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, Form, FormRide, User, Ride, Category, RideCategory
import crud

from jinja2 import StrictUndefined
import webbrowser
import requests
import json 
from pprint import pprint

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
# init_app(app)


@app.route("/")
def welcome_page():
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
    user_profile = session.get("results", {})

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
def rides_page():
    """Show the rides page"""

    res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
    response = res.json()
    pprint(response)

    return render_template("rides.html", rides=response)

@app.route("/filter-ride", methods=["POST"])
def _filter_rides():
    """Private endpoint to create an association object between rides and a category"""
    
    rides = request.form.getlist("ride")
    category = request.form.get("category")
    print(rides, "*****SELECTED RIDES****")
    print(category, "*****SELECTED CATEGORY****")
    
    for ride in rides:
        db_ride = crud.get_ride_by_name(ride)
        print(db_ride, "*****DB RIDE****")
        db_category = crud.get_category_by_name(category)
        print(db_category, "*****DB CATEGORY****")
        db_paired = RideCategory.query.filter_by(ride_id=db_ride.id, category_id=db_category.id).first()
        print(db_paired, "*****DB PAIRED****")
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
    a_dark_ride = bool(request.form.get("q_dark_ride"))
    a_thrill_ride = bool(request.form.get("q_thrill_ride"))
    a_motion_sick = bool(request.form.get("q_motion_sick"))
    a_foodie = bool(request.form.get("q_foodie"))
    a_must_ride_1 = request.form.get("q_must_ride_1")
    a_must_ride_2 = request.form.get("q_must_ride_2")
    a_must_ride_3 = request.form.get("q_must_ride_3")
    print(request.form, "****FORM INPUTS****")


    # WATER_RIDES = ['Splash Mountain', 'Davy Crocketts Explorer Canoes', 'Storybook Land Canal Boats', 'Jungle Cruise']   #variable to hold water rides, can exclude them if weather is cold
    # KID_RIDES = ['Roger Rabbits Car Toon Spin', 'Casey Jr. Circus Train', 'Mickeys House and Meet Mickey', 'Autopia',
    # 'Gadgets Go Coaster', 'Dumbo the Flying Elephant', 'Astro Orbitor', 'King Arthur Carousel', 'Many Adventures of Winnie the Pooh']
    # DARK_RIDES = ['Haunted Mansion', 'Peter Pans Flight', 'Many Adventures of Winnie the Pooh', 
    # "Snow White's Enchanted Wish", 'Pirates of the Caribbean', 'Its a small world', 'Mr Toads Wild Ride', 'Roger Rabbits Car Toon Spin']
    # THRILL_RIDES = ['Matterhorn Bobsleds', 'Big Thunder Mountain Railroad', 'Star Wars: Rise of the Resistance', 'Space Mountain', 'Indiana Jones Adventure', 'Splash Mountain']
    # MOTION_RIDES = ['Millenium Falcon: Smugglers Run', 'Star Tours - The Adventures Continue', 'Finding Nemo Submarine Voyage', 'Space Mountain', 'Mad Tea Party']
    # LARGE_GROUP_RIDES = ['Jungle Cruise', "it's a small world", 'Pirates of the Caribbean', 'Haunted Mansion', 'Pirates Lair on Tom Sawyer Island', 
    # 'Many Adventures of Winnie the Pooh', 'Walt Disneys Enchanted Tiki Room']
    # NO_RIDES = ['Walt Disneys Enchanted Tiki Room', 'Blue Bayou Restaurant', 'Ogas Cantina at the Disneyland Resort', 
    # 'Disneyland Railroad', 'Pooh Corner - Sweets Shop', 'Mint Julep Bar', 'French Market']


    itinerary_set = set()


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

    if a_motion_sick == 'no':
        c_id = crud.get_category_by_name('Motion').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_foodie:
        c_id = crud.get_category_by_name('Foodie').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_must_ride_1:
        c_id = crud.get_category_by_name('Must').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)
    
    if a_must_ride_2:
        c_id = crud.get_category_by_name('Must').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)

    if a_must_ride_3:
        c_id = crud.get_category_by_name('Must').id
        rides = RideCategory.query.filter_by(category_id=c_id).all()
        itinerary_set.update(rides)


    new_profile = Form(user_id=session['pkey'], q_travel_grp=a_travel_grp, q_weather=a_weather, q_dark_ride=a_dark_ride,
                        q_thrill_ride=a_thrill_ride, q_motion_sick=a_motion_sick, q_foodie=a_foodie, q_must_ride_1=a_must_ride_1,
                        q_must_ride_2=a_must_ride_2, q_must_ride_3=a_must_ride_3)   #need to add datetime??    
    db.session.add(new_profile)
    db.session.commit()
    print(new_profile, "****NEW PROFILE****")


    form_id = new_profile.id
    print(form_id)

    for ride_category in itinerary_set:
        saved_result = FormRide(form_id=form_id, ride_id=ride_category.ride.id)
        db.session.add(saved_result)
        db.session.commit()


    return render_template("results.html", itinerary_set=itinerary_set, trip_name=trip_name)

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

    #if user wants to see old itinerary, take them to results route
    #if user wants to fill out a new form, take them to blank form route

    return render_template("user_profile.html") #will need to render new route based on reply



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)