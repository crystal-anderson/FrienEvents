from wtforms import Form, BooleanField, StringField, PasswordField, TextField, ValidationError, SubmitField, validators

from wtforms.validators import DataRequired, Email, EqualTo, Length

from wtforms.fields.html5 import URLField, DateTimeLocalField

from model import User


class RegistrationForm(Form):
    """Registration form referenced on register template and register server route."""

    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    """Login form referenced on login template and login server route."""

    username = TextField('Username',
            validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Unknown username')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True

class UserSearchForm(Form):
    """User Search form referenced on user-search template and user-search server route."""

    username = StringField('',
            validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('User Search')


class CustomAddEventForm(Form):
    """Add event form referenced on add-event template and custom-add-event server route."""

    event_title = StringField('Event Title',
            validators=[DataRequired(), Length(1, 200)])
    event_url = URLField('Event URL',
            validators=[DataRequired(), Length(1, 500)])
    event_date = DateTimeLocalField('Event Date', format='%Y-%m-%dT%H:%M',
            validators=[DataRequired()])
