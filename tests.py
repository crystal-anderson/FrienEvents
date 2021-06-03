# from unittest import TestCase
# from server import app
# from model import connect_to_db, db, example_data
# from flask import session


# class FlaskTestsBasic(TestCase):
#     """Flask tests."""

#     def setUp(self):

#         self.client = app.test_client()

#         app.config['TESTING'] = True


# class FlaskTestsDatabase(TestCase):
#     """Flask tests for the database."""

#     def setUp(self):

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         connect_to_db(app, "postgresql:///frienevents")

#         db.create_all()
#         example_data()

#     def tearDown(self):

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()


# class FlaskTestsLogInLogOut(TestCase):  
#     """Test both log in and log out."""

#     def setUp(self):
#         """Before every test"""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_login(self):
#         """Test log in form."""

#         with self.client as c:
#             result = c.post('/login',
#                             data={'user_id': '123', 'password': 'abc'},
#                             follow_redirects=True
#                             )
#             self.assertEqual(session['user_id'], '123')
#             self.assertIn(b"You are a valued user", result.data)

#     def test_logout(self):
#         """Test logout route."""

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = '123'

#             result = self.client.get('/logout', follow_redirects=True)

#             self.assertNotIn(b'user_id', session)
#             self.assertIn(b'Logged Out', result.data)


# if __name__ == "__main__":
#     import unittest

#     unittest.main()
