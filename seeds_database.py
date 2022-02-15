"""imports api data and seeds it; call function from api_client file"""

"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# os.system("dropdb ratings")
# os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


with open('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime') as f:
    ride_data = json.loads(f.read())


ride_list = []


for ride in ride_data:

    name = ride['name']

    new_ride = crud.create_ride(name)
    ride_list.append(new_ride)


model.db.session.add_all(ride_list)
model.db.session.commit()


model.db.session.commit()
