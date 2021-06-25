from datetime import datetime

from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    surname = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.Integer, default=1)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def is_instructor(self):
        if self.type == 2:
            return True
        
        return False

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    number = db.Column(db.Integer)
    year = db.Column(db.Integer)

    users = db.relationship("User", order_by="User.surname")

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    elapsed_time = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tasks = db.relationship("Task")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Boolean, nullable=False)
