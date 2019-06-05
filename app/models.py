from app import db, login
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    """load user from db"""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """user table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True)
    dateOfBirth = db.Column(db.Date)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(128))
    gender = db.Column(db.String(32))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    training_lists = db.relationship('TrainingList', backref='training_list', lazy='dynamic')
    userinfo = db.relationship('InfoUser', backref='info', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.om/avatar/{}?d=identicon&s={}'.format(digest, size)

    def information_user(self):
        param = InfoUser.query.filter_by(user_id = self.id)
        return param

    def lastinfo_user(self):
        param = InfoUser.query.filter_by(user_id=self.id)
        return param[-1]

class Sport(db.Model):
    """Sport table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    name_sport = db.Column(db.String(256), index=True)
    info = db.Column(db.Text(500), index=True)
    trainings = db.relationship('Training', backref='sport_training', lazy='dynamic')

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

    def __repr__(self):
        return '<Training {}>'.format(self.name_training)


class TrainingList(db.Model):
    """Training list table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    date_finish = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))


#    all_exercises = db.relationship('AllExercises', backref='exercises_list', lazy='dynamic')


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_exercises = db.Column(db.String(256), index=True)
    rules = db.Column(db.Text(500), index=True)


# class UserParametrs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


#
# class AllExercises(db.Model):
#     exercises_id = db.Column(db.Integer, db.ForeignKey('exercises.TypeError: descriptor 'date' of 'datetime.datetime' object needs an argumentid'))
#     training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
#     day = db.Column(db.Integer)
#     count = db.Column(db.Integer)

class InfoUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    arms = db.Column(db.Integer)
    chest = db.Column(db.Integer)
    waist = db.Column(db.Integer)
    femur = db.Column(db.Integer)
    heartDiseases = db.Column(db.String(12))
    date_of_change = db.Column(db.Date, default=datetime.utcnow())
    training_list_id = db.Column(db.Integer, db.ForeignKey('training_list.id'))

