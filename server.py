"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
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

    # this is where i would call the api, very similar to js fetch call
    # 'https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime'

    # for ride in disney_data:
    #     print(disney_data['name'])


    # this worked below
    # res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
    # response = res.json()
    # pprint(response)

    return render_template("rides.html")  #just for me to look at
# , rides=response

@app.route("/form")
def form_page():
    """Loads form for user"""

    return render_template("form.html")

@app.route("/results", methods=['POST'])
def results_page():
    """Shows the results of form"""

    answer_1 = request.form.get("question-1")
    answer_2 = request.form.get("question-2")
    answer_3 = request.form.get("question-3")
    answer_4 = request.form.get("question-4")
    answer_5 = request.form.get("question-5")
    answer_6 = request.form.get("question-6")
    answer_7 = request.form.getlist("question-7")

    itinerary_1 = []
    itinerary_2 = []
    itinerary_3 = []
    itinerary_4 = []

    # if answer_1 is value="Adults; no kids":
    #     itinerary_1 += 1

    # if answer_1 is value="Family; kids under 8":
    #     itinerary_2 += 1

    # if answer_1 is value="Family; kids over 8":
    #     itinerary_3 += 1

    # if answer_1 is value="Large group, 6+":
    #     itinerary_4 += 1



    # if q3_answer is value="yes":



@app.route("/user_itinerary")
def user_itinerary ():
    """User's first page upon second login"""



    return render_template("user_itinerary.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)