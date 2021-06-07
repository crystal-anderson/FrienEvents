from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):

        self.client = app.test_client()

        app.config['TESTING'] = True


class FlaskTestsDatabase(TestCase):
    """Flask tests for the database."""

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///frienevents")

        db.create_all()
        example_data()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


if __name__ == "__main__":
    import unittest

    unittest.main()
