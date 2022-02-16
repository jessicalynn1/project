"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, Form, FormRide, User, Ride
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


    WATER_RIDES = ['Splash Mountain', 'Davy Crocketts Explorer Canoes', 'Storybook Land Canal Boats', 'Jungle Cruise']   #variable to hold water rides, can exclude them if weather is cold
    KID_RIDES = ['Roger Rabbits Car Toon Spin', 'Casey Jr. Circus Train', 'Mickeys House and Meet Mickey', 'Autopia',
    'Gadgets Go Coaster', 'Dumbo the Flying Elephant', 'Astro Orbitor', 'King Arthur Carousel', 'Many Adventures of Winnie the Pooh']
    DARK_RIDES = ['Haunted Mansion', 'Peter Pans Flight', 'Many Adventures of Winnie the Pooh', 
    'Snow Whites Enchanted Wish', 'Pirates of the Caribbean', 'Its a small world', 'Mr Toads Wild Ride', 'Roger Rabbits Car Toon Spin']
    THRILL_RIDES = ['Matterhorn Bobsleds', 'Big Thunder Mountain Railroad', 'Star Wars: Rise of the Resistance', 'Space Mountain', 'Indiana Jones Adventure', 'Splash Mountain']
    MOTION_RIDES = ['Millenium Falcon: Smugglers Run', 'Star Tours - The Adventures Continue', 'Finding Nemo Submarine Voyage', 'Space Mountain', 'Mad Tea Party']
    LARGE_GROUP_RIDES = ['Jungle Cruise', 'Its a small world', 'Pirates of the Caribbean', 'Haunted Mansion', 'Pirates Lair on Tom Sawyer Island', 
    'Many Adventures of Winnie the Pooh', 'Walt Disneys Enchanted Tiki Room']
    NO_RIDES = ['Walt Disneys Enchanted Tiki Room', 'Blue Bayou Restaurant', 'Ogas Cantina at the Disneyland Resort', 
    'Disneyland Railroad', 'Pooh Corner - Sweets Shop', 'Mint Julep Bar', 'French Market']


    itinerary_set = set()


    if a_travel_grp == 'Adults; no kids':
        itinerary_set.update(THRILL_RIDES)

    if a_travel_grp == 'Family; kids under 8':
        itinerary_set.update(KID_RIDES)

    if a_travel_grp == 'Family; kids over 8':
        itinerary_set.update(THRILL_RIDES)
    
    if a_travel_grp == 'Large group, 6+':
        itinerary_set.update(LARGE_GROUP_RIDES)

    if a_weather == 'hot':
        itinerary_set.update(WATER_RIDES)

    if a_dark_ride:
        itinerary_set.update(DARK_RIDES)

    if a_thrill_ride:
        itinerary_set.update(THRILL_RIDES)

    if a_motion_sick == 'no':
        itinerary_set.update(MOTION_RIDES)

    if a_foodie:
        itinerary_set.update(NO_RIDES)

    if a_must_ride_1:
        itinerary_set.add(a_must_ride_1)
    
    if a_must_ride_2:
        itinerary_set.add(a_must_ride_2)

    if a_must_ride_3:
        itinerary_set.add(a_must_ride_3)


    new_profile = Form(user_id=session['pkey'], q_travel_grp=a_travel_grp, q_weather=a_weather, q_dark_ride=a_dark_ride,
                        q_thrill_ride=a_thrill_ride, q_motion_sick=a_motion_sick, q_foodie=a_foodie, q_must_ride_1=a_must_ride_1,
                        q_must_ride_2=a_must_ride_2, q_must_ride_3=a_must_ride_3)       
    db.session.add(new_profile)
    db.session.commit()
    print(session['pkey'])


    saved_result = FormRide()
    db.session.add(saved_result)
    db.session.commit()

    return render_template("results.html", itinerary_set=itinerary_set, trip_name=trip_name)

    # figure out how to email the result to the user in 2.0

# need to send to db, need to create instances of class formride, add those and commit to db


@app.route("/user_profile")
def user_profile():
    """User's first page upon second login"""

    #if user wants to see old itinerary, take them to results route
    #if user wants to fill out a new form, take them to blank form route

    return render_template("user_profile.html") #will need to render new route based on reply



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)