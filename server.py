"""this is where you set up routes (to web pages); routes include functions that return render_templates to html pages"""


from flask import (Flask, render_template, request, flash, session,
                   redirect)
# from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def welcome_page ():
    """Show the Welcome page"""

    return render_template("template.html")

@app.route("/")
def rides_page ():
    """Show the itinerary page"""

    return render_template("template.html")

if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)