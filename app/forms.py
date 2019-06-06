from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, BooleanField,SelectField
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
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    weight = StringField('Вес', validators=[DataRequired()])
    height = StringField('Рост', validators=[DataRequired()])
    arms = StringField('Бицепс', validators=[DataRequired()])
    chest = StringField('Грудь', validators=[DataRequired()])
    waist = StringField('Талия', validators=[DataRequired()])
    femur = StringField('Бедро', validators=[DataRequired()])
    heartDiseases = SelectField('Наличие сердечных заболеваний',  choices = [('No','Нет'),('Yes','Да')])

    submit = SubmitField('Обновить')

class SelectTrainingForm(FlaskForm):
    tipe = SelectField('Выберите тип тренировки', choices=[('no', 'Не важно'),
                                                           ('Для начинающих', 'для начинающих'),
                                                           ('Для профессионалов', 'Для профессионалов')])
    muscle_group = SelectField('Выберите группу мышц', choices=[('no', 'Не важно'),
                                                                ('Все тело', 'Все тело'),
                                                                ('Ноги', 'Ноги'),
                                                                ('Руки', 'Руки'),
                                                                ('Пресс', 'Пресс')])

    name_sport = SelectField('Выберите вид спорта', choices=[('no', 'Не важно'),
                                                                ('Теннис', 'Теннис'),
                                                                ('Легкая атлетика', 'Легкая атлетика'),
                                                                ('Футбол', 'Футбол')])
    submit = SubmitField('Подобрать тренировку!')