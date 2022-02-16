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


res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
response = res.json()
# pprint(response)

ride_list = []

for ride in response:

    name = ride['name']

    new_ride = crud.create_ride(name)
    ride_list.append(new_ride)


model.db.session.add_all(ride_list)
model.db.session.commit()

