"""imports api data and seeds it; call function from api_client file"""

"""Script to seed database."""

import os
import json
from random import choice, randint
import requests
from pprint import pprint

import crud
import model
import server


model.connect_to_db(server.app)
model.db.create_all()


categories = ["Dark", "Water", "Thrill", "Adults", "Kid", "Motion", "Foodie", "Large Group", "Must"]

for category in categories:
    c = model.Category(name=category)
    model.db.session.add(c)
    model.db.session.commit()

res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
response = res.json()

for ride in response:
    name = ride['name']
    new_ride = crud.create_ride(name)
    model.db.session.add(new_ride)
    model.db.session.commit()

