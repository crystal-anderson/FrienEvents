"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system('dropdb frienevents')
os.system('createdb frienevents')

model.connect_to_db(server.app)
model.db.create_all()


with open('data/events.json') as f:
    event_data = json.loads(f.read())

events_in_db = []
for event in event_data:
    usr_desc, site_title, event_url = (
        event["usr_desc"],
        event["site_title"],
        event["event_url"],
    )
    event_date = datetime.strptime(event["event_date"], "%m-%d-%Y")

    db_event = crud.create_event(usr_desc, site_title, event_date, event_url)
    events_in_db.append(db_event)