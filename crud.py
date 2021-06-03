"""CRUD operations."""

from model import db, connect_to_db


def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)

    db.session.add(user)
    db.session.commit()

    return user


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


def create_comment(user, event, comment, comment_date):
    """Create and return a new comment."""

    comment = Comment(
        user=user,
        event=event,
        comment=comment,        
        comment_date=comment_date,
    )

    db.session.add(comment)
    db.session.commit()

    return rating


def create__users_events(user, event):
    """Create and return a new users_events."""


    users_events = UserEvent(
        user=user,
        event=event,
    )

    db.session.add(users_events)
    db.session.commit()

    return users_events


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    