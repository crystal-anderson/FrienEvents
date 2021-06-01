"""Models for FrienEvents app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


#


if __name__ == '__main__':
    from server import app

    connect_to_db(app)