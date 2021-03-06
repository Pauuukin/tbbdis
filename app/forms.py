from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, BooleanField,SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,Length
from app.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()]) # валидатор проверяет, что поле не пусто
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Выберите пол',  choices = [('Мужской','Мужской'),('Женский','Женский')])
    age = StringField('Количество лет', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')])
    rules = RadioField(choices = [('П','Ознакомился(-лась) с соглашением и принимаю правила сайта'),('О','Отказываюсь')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, выберите другое имя.')


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Такой Email уже зарегистрирован! Пожалуста, введите другой.')

class EditProfileForm(FlaskForm):
    weight = StringField('Вес', validators=[DataRequired()])
    height = StringField('Рост', validators=[DataRequired()])
    arms = StringField('Обхват бицепса')
    shoulder = StringField('Обхват плеч')
    chest = StringField('Обхват груди')
    waist = StringField('Обхват талии')
    femur = StringField('Обхват бёдер')
    heartDiseases = SelectField('Наличие сердечных заболеваний',  choices = [('No','Нет'),('Yes','Да')])

    submit = SubmitField('Обновить')

class SelectTrainingForm(FlaskForm):
    tipe = SelectField('Выберите тип тренировки', default=  'Не важно', choices=[('Нет', 'Не важно'),
                                                           ('Для начинающих', 'Для начинающих'),
                                                           ('Для профессионалов', 'Для профессионалов')])
    muscle_group = SelectField('Выберите группу мышц', choices=[('Нет', 'Не важно'),
                                                                ('Все тело', 'Все тело'),
                                                                ('Ноги', 'Ноги'),
                                                                ('Руки', 'Руки'),
                                                                ('Пресс', 'Пресс')])

    name_sport = SelectField('Выберите вид спорта', choices=[('Нет', 'Не важно'),
                                                                ('Теннис', 'Теннис'),
                                                                ('Легкая атлетика', 'Легкая атлетика'),
                                                                ('Футбол', 'Футбол')])
    submit = SubmitField('Подобрать тренировку!')


class AcceptTrainingForm(FlaskForm):
    submit = SubmitField('Принять тренировку!')


class CompleteExeForm(FlaskForm):
    submit = SubmitField('Готово!')