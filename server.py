"""Server for FrienEvents app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
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

# /// THIS IS TO COME ///
# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     user = User.query.filter_by(username=username).first()

#     if user.password == password:
#         login_user(user)

#         flash("Logged in successfully!")

#         return redirect("/dashboard")

#     flash("Sorry try again.")
#     return redirect("/")


# /// NOT YET, BUT TO MAKE A LOGIN REQUIRED ///
# @app.route("/calendar")
# @login_required
# def calendar():
#     return render_template("calendar.html")

# /// JINJA TEMPLATE FOR PAGE ///
# {% if current_user.is_authenticated %}
#   Hi there {{ current_user.first_name }}!
# {% endif %}


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    