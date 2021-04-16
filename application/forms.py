from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    assignee = SelectField('Assignee for the Task', choices=[], validators=[DataRequired()])
    description = StringField('Description of the Task', validators=[DataRequired()])
    submit = SubmitField('Add Task')

class AssigneeForm(FlaskForm):
    forename = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    submit = SubmitField('Add Assignee')