"""Models for FrienEvents app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///frienevents', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    # event_id = 
    #           // LINK TO EVENTS TABLE
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email}>'


class Comment(db.Model):
    """A comment."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    comment = db.Column(db.Text)
    # user_id = 
    #         // LINK TO USER TABLE
    comment_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} comment={self.comment} comment_date={comment_date}'


class Event(db.Model):
    """An event."""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    usr_desc = db.Column(db.Text)
    site_title = db.Column(db.String)
    event_date = db.Column(db.DateTime)
    event_url = db.Column(db.String)


class Calendar(db.Model):
    """This allows for multiple events to be tied to multiple users. Many to many."""

    __tablename__ = 'calendars'

    calendar_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    # user_id = 
    #         // LINK TO USER TABLE
    # event_id = 
    #         // LINK TO EVENT TABLE



if __name__ == '__main__':
    from server import app

    connect_to_db(app)