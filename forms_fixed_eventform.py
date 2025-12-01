from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    venue = StringField("Venue", validators=[DataRequired()])
    start_time = DateTimeField("Start Time (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
    end_time = DateTimeField("End Time (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    image = FileField("Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
    submit = SubmitField("Create Event")
