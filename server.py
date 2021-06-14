"""Server for FrienEvents app."""

from flask import Flask, redirect, render_template, request, flash, session
from model import connect_to_db, db, User
from form import RegistrationForm, LoginForm
import crud
import os
import requests
import json

from wtforms import Form, BooleanField, StringField, validators
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = 'frieneventsdev'
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

API_KEY = os.environ['TICKETMASTER_KEY']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    """View homepage."""

    if session.get('current_user'):
        username = session['current_user']
        user = crud.get_user_by_username(username)

    return render_template('homepage.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration form."""

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        crud.create_user(form.email.data, form.password.data, form.username.data)
        flash('Thanks for registering')

        return redirect('login')

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logout the current user."""

    logout_user()
    if current_user.is_authenticated:
        # prevent flashing automatically logged out message
        del session['current_user']
    flash('You have successfully logged yourself out.')

    return redirect('/')


@app.route('/search')
def search_events():
    """Search for events."""

    keyword = request.args.get('keyword', '')

#    TODO verify these are valid arguments 
    city = request.args.get('city', '')
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')
    statecode = request.args.get('stateCode', '')
    sort = request.args.get('sort', '')
    
    start_end_datetime = []
    if startdate:
        start_end_datetime.append(startdate)
    if enddate:
        start_end_datetime.append(enddate)

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
               'keyword': keyword,
               'localStartEndDateTime': ', '.join(start_end_datetime),
               'city': city,
               'stateCode': statecode,
               'sort': sort}

    response = requests.get(url, params=payload)

    data = response.json()

    events = data["_embedded"]["events"]

    return render_template('search-results.html', events=events)


@app.route('/calendar')
@login_required
def calendar():
    """View calendar page."""

    if session.get('current_user'):
        user = crud.get_user_by_username(session['current_user'])
        user_events = crud.get_users_events_by_user_id(user.user_id)

        events_list = []

        for user_event in user_events:
            event = crud.get_event_by_id(user_event.event_id)

            # TODO sort by date to new list

            events_list.append({"title" : event.site_title, "date" : event.event_date, "url" : event.event_url, "desc" : user_event.user_desc})

        return render_template('calendar.html', user=user,  events_list=events_list)
    
    else:
        return redirect('/')


@app.route('/addevent', methods=['POST'])
def add_event():
    """Add event from search event results to user calendar."""

    if session.get('current_user'):
        user = crud.get_user_by_username(session['current_user'])
        
        events_to_add = request.form.getlist('events-to-add')
        event_data = []
        for evt in events_to_add:
            event_data.append(json.loads(evt))


        for event in event_data:
            new_event = crud.create_event(event["site_title"], event["event_date"], event["event_url"])
            user.calendar.append(new_event)
        
        db.session.add(user)
        db.session.commit()

        return render_template('homepage.html')
    
    else:
        return redirect('login.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    