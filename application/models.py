from application import db
from datetime import datetime

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignees.id'), nullable=False)

class Assignees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Tasks', backref='assignee')
    