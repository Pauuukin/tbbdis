from app import db, login
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import and_


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
    active_training = db.Column(db.Integer, default = 0)

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
        param = InfoUser.query.filter_by(user_id=self.id)
        return param

    def lastinfo_user(self):
        param = InfoUser.query.filter_by(user_id=self.id)
        return param[-1]


# class Sport(db.Model):
#     """Sport table in sqlalchemy"""
#     id = db.Column(db.Integer, primary_key=True)
#     name_sport = db.Column(db.String(256), index=True)
#     info = db.Column(db.Text(500), index=True)
#     trainings = db.relationship('Training', backref='sport_training', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Sport {}>'.format(self.name_sport)


class Training(db.Model):
    """Training list table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    name_training = db.Column(db.String(256), index=True)
    tipe = db.Column(db.String(256))
    muscle_group = db.Column(db.String(256))
    gender = db.Column(db.String(32))
    count_day = db.Column(db.Integer)
    name_sport = db.Column(db.String(64))
    exercises_list = db.relationship('Exercises', backref='exe', lazy='dynamic')

    def __repr__(self):
        return '<Training {}>'.format(self.name_training)

    def all_exe(self):
        """выводим все упражнения по данной тренировке"""
        exe = Exercises.query.filter_by(training_id=self.id)
        return exe

    def day_exe(self, day):
        """выводим упражнение по конкретному дню"""
        exe = Exercises.query.filter((Exercises.training_id == self.id) & (Exercises.day == day))
        return exe

    def all_training(self):
        t = Training.query.all()
        return t

    def search_training(self):
        """первоначальная выборка тренировок"""
        selected_training = Training.query.filter(Training.gender == self.gender).filter((Training.muscle_group == self.muscle_group) & (Training.name_sport == self.name_sport) & (Training.tipe == self.tipe))
        return selected_training


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_exercises = db.Column(db.String(256), index=True)
    rules = db.Column(db.Text(500), index=True)
    day = db.Column(db.Integer)
    number = db.Column(db.Integer)
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))


class TrainingList(db.Model):
    """Training list table in sqlalchemy"""
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    date_finish = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))

    def get_training(self):
        selected_training = TrainingList.query.filter_by(user_id = self.user_id)
        return selected_training[-1]


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
