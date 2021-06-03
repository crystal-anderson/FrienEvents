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
crud.create_event('Austin City Limits', 'ACL Music Festival - Weekend 1', '2021-10-2', 'https://www.aclfestival.com/', '1')
crud.create_event('Austin City Limits', 'ACL Music Festival - Weekend 2', '2021-10-8', 'https://www.aclfestival.com/', '1')
crud.create_comment('1', '1', 'Very excited for music, beer, and rivers!', '2021-05-03')
crud.create_users_events('1', '1')
crud.create_users_events('1', '2')
crud.create_users_events('2', '2')

#more random users
#RANDOM USERS FOR TEST SERVER
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"
    username = f"{n}"

    user = crud.create_user(email, password, username)


with open('data/events.json') as f:
    event_data = json.loads(f.read())

events_in_db = []
for event in event_data:
    usr_desc, site_title, event_url, user_id = (
        event["usr_desc"],
        event["site_title"],
        event["event_url"],
        event["user_id"]
    )
    event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")

    db_event = crud.create_event(usr_desc, site_title, event_date, event_url, user_id)
    events_in_db.append(db_event)
