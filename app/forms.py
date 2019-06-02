from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,Length
from app.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # валидатор проверяет, что поле не пусто
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

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
#    heartDiseases = BooleanField('Сердечные заболевания', validators=[DataRequired()])
#    date_of_change = StringField(validators=[DataRequired()],default=datetime.utcnow())
    submit = SubmitField('Обновить')
