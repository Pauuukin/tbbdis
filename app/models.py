from app import db
from datetime import datetime

class User(db.Model):
    """user table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), index = True)
    dateOfBirth = db.Column(db.Date)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(128))
    gender = db.Column(db.String(32))
    training_lists = db.relationship('TrainingList', backref='training_list', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Sport(db.Model):
    """Sport table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    name_sport = db.Column(db.String(256), index=True)
    info = db.Column(db.Text(500), index=True)
    trainings = db.relationship('Training', backref = 'sport_training', lazy = 'dynamic')

    def __repr__(self):
        return '<Sport {}>'.format(self.name_sport)


class Training(db.Model):
    """Training list table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    name_training = db.Column(db.String(256), index=True)
    tipe = db.Column(db.String(256))
    muscle_group = db.Column(db.String(256))
    gender = db.Column(db.String(32))
    count_day = db.Column(db.Integer)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    training_lists = db.relationship('TrainingList', backref='training_list', lazy='dynamic')

    def __repr__(self):
        return '<Training {}>'.format(self.name_training)



class TrainingList(db.Model):
    """Training list table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, index = True, default = datetime.utcnow())
    date_finish = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    all_exercises = db.relationship('AllExercises', backref='exercises_list', lazy='dynamic')


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_exercises = db.Column(db.String(256), index=True)
    rules = db.Column(db.Text(500), index=True)

# class UserParametrs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)



#
# class AllExercises(db.Model):
#     exercises_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
#     training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
#     day = db.Column(db.Integer)
#     count = db.Column(db.Integer)