"""Server for FrienEvents app."""

from flask import Flask, redirect, render_template, request, flash, session, jsonify
from model import connect_to_db, db, User, Event
from form import RegistrationForm, LoginForm, UserSearchForm, CustomAddEventForm
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

    if crud.get_user_by_email(form.email.data):
        flash(f'Account already created with the email {form.email.data}')
        return redirect('/login')

    if crud.get_user_by_username(form.username.data):
        flash(f'Account already created with the username {form.username.data}')
        return redirect('/login')

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
    sort = request.args.get('sort', 'relevance,asc')

    start_end_datetime = []
    if startdate:
        start_end_datetime.append(startdate)
    if enddate:
        start_end_datetime.append(enddate)

    print('\n\n\n\n\n')
    print(startdate)
    
    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
               'keyword': keyword,
               'localStartEndDateTime': ', '.join(start_end_datetime),
               'city': city,
               'stateCode': statecode,
               'sort': sort,
               'size': '100'}

    response = requests.get(url, params=payload)

    data = response.json()

    if "_embedded" in data and "events" in data["_embedded"]:

        return render_template('search-results.html', events=data["_embedded"]["events"])

    flash('No results found. Update search criteria.')
    return redirect('/')


@app.route('/add-event', methods=['POST'])
def add_event():
    """Add event from search event results to user calendar."""

    if current_user.is_authenticated:
        events_to_add = request.form.getlist('events-to-add')

        for evt in events_to_add:
            data = json.loads(evt)
            event = crud.create_event(data["event_title"], data["event_date"], data["event_url"])
            current_user.events.append(event)
            db.session.commit()

        return redirect ('/calendar')

    else:
        return redirect('/login')


@app.route('/api/remove-event/<int:event_id>', methods=['POST'])
def remove_event(event_id):
    """Add event from search event results to user calendar."""

    # Get event to loop over associated user_events
    event = Event.query.get(event_id)

    for user_event in event.user_events:

        if user_event.user_id == current_user.user_id:
            db.session.delete(user_event)
            db.session.commit()

            return f"Removed user_event with ID: {user_event.user_event_id} for event {event_id}"

    print(f"COULDN'T FIND EVENT TO DELETE :(")

    return "Error"


@app.route('/calendar')
@login_required
def calendar():
    """View calendar page."""

    if current_user.is_authenticated:
        user = crud.get_user_by_username(current_user.username)

        return render_template('calendar.html', user=user, current_user=current_user)

    else:
        return redirect('/')


@app.route('/api/user/<user_id>/events')
def get_users_events(user_id):
    """Json data format to render calendar."""

    events_list = []
    user = crud.get_user_by_id(user_id)

    for event in user.events:
        events_list.append({
            "event_id": event.event_id,
            "title" : event.event_title,
            "start" : event.event_date.isoformat(),
            "url" : event.event_url,
            # "description": event.user_events[0].user_desc
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


@app.route('/custom-add-event', methods=['GET', 'POST'])
def custom_add_event():
    """View add event page with form to manually add an event."""

    form = CustomAddEventForm(request.form)

    if current_user.is_authenticated:
        user = crud.get_user_by_username(current_user.username)

        if request.method == 'POST':

            event = crud.create_event(form.event_title.data, 
                                        form.event_date.data, 
                                        form.event_url.data)
            user.events.append(event)
            db.session.commit()
            flash('Your event has been added!')

            return redirect('/calendar')

    return render_template('add-event.html', user=user, form=form)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
