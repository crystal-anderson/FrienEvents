"""Models for FrienEvents app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(20))
    username = db.Column(db.String(20))

    comments = db.relationship('Comment', backref='users')

    def get_id(self):
        """Overrride UserMixin.get_id."""

        return str(self.user_id)

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
    usr_desc = db.Column(db.Text)
    site_title = db.Column(db.String(50))
    event_date = db.Column(db.DateTime)
    event_url = db.Column(db.String(200))

    comments = db.relationship('Comment', backref='events')

    def __repr__(self):
        return f'<Event || event_id={self.event_id} // user_desc={self.usr_desc} // event_date={self.event_date}>'


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

    def __repr__(self):
        return f'<UserEvent || user_event_id={self.user_event_id} user_id={self.user_id} event_id={self.event_id}>'

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


#TO DO
#SeedDatabase?! Change from 'import model' to 'from model import db'?
#Add comment key to Users_Events instead of User.
