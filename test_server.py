"""test to make sure your code is working"""

from unittest import TestCase
import json
from server import app
import server
from model import User, Ride, Category, Form, RideCategory, FormRide, connect_to_db, db, example_data
from flask_sqlalchemy import SQLAlchemy
client = app.test_client()


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)
    
    def test_login_route(self):
        """Test login route."""

        result = self.client.get("/login")
        self.assertIn(b"Log In", result.data)

class FlaskTests(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""    
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def find_category(self):
        """Search for category in table"""

        adults = Category.query.filter(Category.name == "Adults").first()
        self.assertEqual(adults.name, "Adults")

    def find_ride(self):
        """Search for ride in table"""

        haunted_mansion = Ride.query.filter(Ride.name == "Haunted Mansion").first()
        self.assertEqual(haunted_mansion.name, "Haunted Mansion")


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'dev'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_form_page(self):
        """Test form page."""

        result = self.client.get("/form")
        self.assertIn(b"fill out the form", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_profile_page(self):
        """Test that user can't see profile page when logged out."""

        result = self.client.get("/", follow_redirects=True)
        self.assertNotIn(b"saved itinerary", result.data)
        self.assertIn(b"Log In", result.data)

if __name__ == "__main__":
    import unittest
    unittest.main()
