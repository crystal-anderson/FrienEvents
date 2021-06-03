"""CRUD operations."""

from model import db, User, Comment, Event, UserEvent, connect_to_db


def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)

    db.session.add(user)
    db.session.commit()

    return user


def create_event(usr_desc, site_title, event_date, event_url, user_id):
    """Create and return a new event."""


    event = Event(
        usr_desc=usr_desc,
        site_title=site_title,
        event_date=event_date,
        event_url=event_url,
        user_id=user_id
    )

    db.session.add(event)
    db.session.commit()

    return event


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


def create_users_events(user_id, event_id):
    """Create and return a new users_events."""


    users_events = UserEvent(
        user_id=user_id,
        event_id=event_id,
    )

    db.session.add(users_events)
    db.session.commit()

    return users_events


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    