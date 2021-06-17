"""Server for FrienEvents app."""

from flask import Flask, redirect, render_template, request, flash, session, jsonify
from model import connect_to_db, db, User
from form import RegistrationForm, LoginForm, UserSearchForm
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

os.system('source secrets.sh')
API_KEY = os.environ['TICKETMASTER_KEY']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    """View homepage with event search form."""

    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """View login page. Log user in."""

    form = LoginForm(request.form)

    if  request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
       
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/')
    
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration form."""

    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        crud.create_user(form.email.data, form.password.data, form.username.data)
        flash('Thanks for registering')

        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logout the current user."""

    logout_user()

    flash('You have successfully logged out.')

    return redirect('/')


@app.route('/search')
def search_events():
    """Search for events."""

    keyword = request.args.get('keyword', '')
    city = request.args.get('city', '')
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')
    statecode = request.args.get('stateCode', '')
    sort = request.args.get('sort', 'date,desc')
    
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

    if "_embedded" in data and "events" in data["_embedded"]:

        return render_template('search-results.html', events=data["_embedded"]["events"])

    flash('No results found. Update search criteria.')
    return redirect('/')


@app.route('/addevent', methods=['POST'])
def add_event():
    """Add event from search event results to user calendar."""

    if current_user.is_authenticated:
        user = crud.get_user_by_username(current_user.username)
        events_to_add = request.form.getlist('events-to-add')

        for evt in events_to_add:
            data = json.loads(evt)
            event = crud.create_event(data["site_title"], data["event_date"], data["event_url"])
            user.calendar.append(event)
            db.session.commit()      

        return redirect ('calendar') #TODO update to add event
    
    else:
        return redirect('/login')


@app.route('/calendar')
@login_required
def calendar():
    """View calendar page."""

    if current_user.is_authenticated:
        user = crud.get_user_by_username(current_user.username)
        
        return render_template('calendar.html', user=user)
    
    else:
        return redirect('/')


@app.route('/calendar.json/<user_id>', methods=['POST'])
def calendar_data(user_id):
    """Data format to render calendar."""

    events_list = []

    user_events = crud.get_users_events_by_user_id(user_id)

    for user_event in user_events:
        event = crud.get_event_by_id(user_event.event_id)
        events_list.append({
            "title" : event.site_title, 
            "start" : event.event_date.isoformat(), 
            "url" : event.event_url
            })

    return jsonify(events_list)


@app.route('/user-search', methods=['GET', 'POST'])
def user_search():
    """User search"""

    form = UserSearchForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            flash('No results found!')
            return redirect('/user-search')
        
        else:
            return render_template('calendar.html', user=user)

    return render_template('user-search.html', form=form)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    