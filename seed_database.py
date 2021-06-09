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
crud.create_user('cryssann@gmail.com', 'theusualpassword', 'tatchsnart')
crud.create_user('namesmadly@gmail.com', 'herusualpassword', 'namesmadly')
# crud.create_event('Austin City Limits', 'ACL Music Festival - Weekend 1', '2021-10-2', 'https://www.aclfestival.com/', '1')
# crud.create_event('Austin City Limits', 'ACL Music Festival - Weekend 2', '2021-10-8', 'https://www.aclfestival.com/', '1')


with open('data/events.json') as f:
    event_data = json.loads(f.read())

events_in_db = []
for event in event_data:
    site_title, event_date, event_url = (
        event["site_title"],
        event["event_date"],
        event["event_url"]
    )
    event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")

    db_event = crud.create_event(site_title, event_date, event_url)
    events_in_db.append(db_event)

#tying random input for testing
crud.create_comment('1', '1', 'Very excited for music, beer, and rivers!', '2021-05-03')
crud.create_users_events('1', '1', 'Weekend 1 baby!')
crud.create_users_events('1', '2', 'Excited to go with you!')
crud.create_users_events('2', '2', 'sgonna be fun!')