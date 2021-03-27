from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    classificationName = StringField('Genre', validators=[DataRequired()])
    postalCode = StringField("Zip Code", validators=[Length(5)])
    submit = SubmitField('Submit')