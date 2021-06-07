"""Server for FrienEvents app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, User
import crud

from flask_login import LoginManager, login_user, login_required

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "frieneventsdev"
app.jinja_env.undefined = StrictUndefined


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/login')
def show_login_page():
    """View login page."""

    return render_template('login.html')


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

    if get_user_by_email(email):
        flash(f'Account already created with {email}')
        return redirect('/login')

    if get_user_by_username(username):
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
    