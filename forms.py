"""
forms.py
"""

from flask_wtf import Form
from wtforms import IntegerField, DecimalField
from wtforms.validators import NumberRange

class StepNumForm(Form):
    step_num = IntegerField("Number of steps", validators=[NumberRange(1,10)])

class LocationForm(Form):
    latitude = DecimalField("Latitude", validators=[NumberRange(-180, 180)])
    longitude = DecimalField("Longitude", validators=[NumberRange(-90, 90)])

class CombinedForm(Form):
    step_num = IntegerField("Number of steps", validators=[NumberRange(1,10)])
    latitude = DecimalField("Latitude", validators=[NumberRange(-180, 180)])
    longitude = DecimalField("Longitude", validators=[NumberRange(-90, 90)])
