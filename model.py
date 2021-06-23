"""Models for FrienEvents app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from wtforms import Form, BooleanField, StringField, PasswordField, validators


db = SQLAlchemy()

class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String,
                        unique=True,
                        nullable=False)
    password = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)

    comments = db.relationship('Comment', backref='users')
    events = db.relationship('Event', secondary='users_events', backref='users')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def verify_password(self, password):
        return (password)

    def get_id(self):
        """Overrride UserMixin.get_id."""

        return str(self.user_id)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):

        return f'<User || user_id={self.user_id} // username={self.username} // email={self.email}>'


class Comment(db.Model):
    """A comment."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    comment = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    event_id = db.Column(db.Integer,
                        db.ForeignKey('events.event_id'),
                        nullable=False)

    def __repr__(self):
        return f'<Comment || comment_id={self.comment_id} // comment={self.comment} // comment_date={self.comment_date}>'


class Event(db.Model):
    """An event."""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    event_title = db.Column(db.String(100))
    event_date = db.Column(db.DateTime)
    event_url = db.Column(db.String(200))

    comments = db.relationship('Comment', backref='events')

    def __repr__(self):
        return f'<Event || event_id={self.event_id} // event_date={self.event_date}>'


class UserEvent(db.Model):
    """This allows for multiple events to be tied to multiple users. Many to many."""

    __tablename__ = 'users_events'

    user_event_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    event_id = db.Column(db.Integer,
                        db.ForeignKey('events.event_id'),
                        nullable=False)

    user_desc = db.Column(db.Text)

    event = db.relationship('Event', backref="user_events")

    def __repr__(self):
        return f'<UserEvent || user_event_id={self.user_event_id} user_id={self.user_id} event_id={self.event_id} user_desc={self.user_desc}>'

def connect_to_db(flask_app, db_uri='postgresql:///frienevents', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)

