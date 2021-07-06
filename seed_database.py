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


#random input for testing
crud.create_user('self.crystal.ann@gmail.com', 'theusualpassword', 'crystal')
crud.create_user('self.ashley@gmail.com', 'theirusualpassword', 'ashley')


with open('data/events.json') as f:
    event_data = json.loads(f.read())

events_in_db = []
for event in event_data:
    event_title, event_date, event_url = (
        event["event_title"],
        event["event_date"],
        event["event_url"]
    )
    event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")

    db_event = crud.create_event(event_title, event_date, event_url)
    events_in_db.append(db_event)

#tying random input for testing
crud.create_comment('1', '1', 'Very excited for music, beer, and rivers!', '2021-05-03')
crud.create_users_events('1', '1', 'Weekend 1 baby!')
crud.create_users_events('1', '2', 'Excited to go with you!')
crud.create_users_events('2', '2', 'sgonna be fun!')