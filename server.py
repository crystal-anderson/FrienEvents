"""Server for FrienEvents app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, User
import crud
import os
import requests

from pprint import pformat

from flask_login import LoginManager, login_user, current_user, login_required, logout_user

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

    return render_template('homepage.html')


@app.route('/search')
def search_events():
    """Search for events."""

    keyword = request.args.get('keyword', '')
   
#    TODO verify these are valid arguments 
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
               'keyword': keyword,
               'postalCode': postalcode,
               'radius': radius,
               'unit': unit,
               'sort': sort}

    response = requests.get(url, params=payload)

    data = response.json()

    events = data["_embedded"]["events"]

    return render_template('search-results.html', events=events)


@app.route('/login')
def show_login_page():
    """View login page."""

    if session.get('current_user'):
        username = session['current_user']
        user = crud.get_user_by_username(username)
        flash(f'Already logged in as {username}')
        return render_template('homepage.html', user=user)
    
    else:
        return redirect('/login')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""

    logout_user()

    return render_template("login.html")


@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log user into application."""

    username = request.form.get('username')
    password = request.form.get('password')
    user = crud.get_user_by_username(username)

    if password == crud.get_password_by_username(username):
        session['current_user'] = username
        login_user(user)
        flash(f'Logged in as {username}')
        return redirect('/')

    else:
        flash('Wrong password!')
        return redirect('/login')


@app.route('/register-user', methods=['POST'])
def register_user():
    """Register user to application."""

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash(f'Account already created with {email}')
        return redirect('/login')

    if crud.get_user_by_username(username):
        flash(f'Account already created with {username}')
        return redirect('/login')

    crud.create_user(email, password, username)
    
    return redirect('/login')


@app.route('/calendar')
@login_required
def calendar():
    """View calendar page."""

    if session.get('current_user'):
        username = session['current_user']
        user = crud.get_user_by_username(username)
        return render_template('calendar.html', user=user)
    
    else:
        return redirect('/login')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    