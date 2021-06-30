from wtforms import Form, BooleanField, StringField, PasswordField, TextField, ValidationError, SubmitField, validators

from wtforms.validators import DataRequired, EqualTo, Length

from wtforms.fields.html5 import EmailField, URLField, DateTimeLocalField

from model import User


class RegistrationForm(Form):
    """Registration form referenced on register template and register server route."""

    username = StringField('username', validators=[DataRequired(), Length(1, 64)])
    email = EmailField('email address', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('new password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords must match')
    ])
    confirm = PasswordField('repeat password')
    accept_tos = BooleanField('I will go on an adventure ♥', [validators.DataRequired()])


class LoginForm(Form):
    """Login form referenced on login template and login server route."""

    username = TextField('username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('log in')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('unknown username')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('invalid password')
            return False
        return True

class UserSearchForm(Form):
    """User Search form referenced on user-search template and user-search server route."""

    username = StringField('username',
            validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('User Search')


class CustomAddEventForm(Form):
    """Add event form referenced on add-event template and custom-add-event server route."""

    event_title = StringField('event title',
            validators=[DataRequired(), Length(1, 200)])
    event_url = URLField('event URL',
            validators=[DataRequired(), Length(1, 500)])
    event_date = DateTimeLocalField('event date', format='%Y-%m-%dT%H:%M',
            validators=[DataRequired()])
