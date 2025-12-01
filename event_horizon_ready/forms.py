from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length

# -------------------------
# Registration Form
# -------------------------
class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

# -------------------------
# Login Form
# -------------------------
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# -------------------------
# Event Form (Admin)
# -------------------------
class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    venue = StringField("Venue")
    start_time = DateTimeField("Start Time", format="%Y-%m-%d %H:%M")
    end_time = DateTimeField("End Time", format="%Y-%m-%d %H:%M")
    capacity = IntegerField("Capacity")
    image = FileField("Event Image")
    submit = SubmitField("Create Event")
