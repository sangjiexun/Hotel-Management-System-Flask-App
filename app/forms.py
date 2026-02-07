from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Team, Room

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    team_id = SelectField('Team', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# Room form
class RoomForm(FlaskForm):
    name = StringField('Room Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    equipment = TextAreaField('Equipment')
    location = StringField('Location', validators=[DataRequired()])
    availability = BooleanField('Availability')
    submit = SubmitField('Save')

# Meeting form
class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    participants = SelectField('Participants', coerce=int, validators=[DataRequired()], choices=[], render_kw={'multiple': True})
    partners = SelectField('Business Partners', coerce=int, choices=[], render_kw={'multiple': True})
    submit = SubmitField('Schedule')

# Team form
class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

# Cost log form
class CostLogForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Cost')

# Business partner form
class BusinessPartnerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person')
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone')
    address = TextAreaField('Address')
    submit = SubmitField('Save')