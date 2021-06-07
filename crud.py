"""CRUD operations."""

from model import db, User, Comment, Event, UserEvent, connect_to_db


def create_user(email, password, username):
    """Create and return a new user."""

    user = User(email=email, password=password, username=username)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).all()


def get_user_by_username(username):
    """Return a user by username."""

    return User.query.filter(User.username == username).first()


def get_password_by_username(username):
    """Return a password by username."""

    username = User.query.filter(User.username == username).first()

    return username.password


def create_event(usr_desc, site_title, event_date, event_url):
    """Create and return a new event."""


    event = Event(
        usr_desc=usr_desc,
        site_title=site_title,
        event_date=event_date,
        event_url=event_url,
    )

    db.session.add(event)
    db.session.commit()

    return event

def get_events():
    """Return all events."""

    return Event.query.all()


def get_event_by_id(event_id):
    """Return an event by primary key."""

    return Event.query.get(event_id)



def create_comment(user_id, event_id, comment, comment_date):
    """Create and return a new comment."""

    comment = Comment(
        user_id=user_id,
        event_id=event_id,
        comment=comment,        
        comment_date=comment_date,
    )

    db.session.add(comment)
    db.session.commit()

    return comment

def get_comments():
    """Return all comments."""

    return Comment.query.all()

def get_comments_by_user_id(user_id):
    """Return comments by users primary key."""

    return Comment.query.filter(Comment.user_id == user_id).all()

def get_comments_by_event_id(event_id):
    """Return comments by events primary key."""

    return Comment.query.filter(Comment.event_id == event_id).all()


def create_users_events(user_id, event_id):
    """Create and return a new users_events."""


    users_events = UserEvent(
        user_id=user_id,
        event_id=event_id,
    )

    db.session.add(users_events)
    db.session.commit()

    return users_events


def get_users_events():
    """Return all users events."""

    return UserEvent.query.all()


def get_users_events_by_user_id(user_id):
    """Return events by users primary key."""

    return UserEvent.query.filter(UserEvent.user_id == user_id).all()

def get_users_events_by_event_id(event_id):
    """Return events by events primary key."""

    return UserEvent.query.filter(UserEvent.event_id == event_id ).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

