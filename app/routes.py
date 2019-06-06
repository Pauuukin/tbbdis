from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SelectTrainingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, InfoUser, Training, Exercises
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required  # запрещает назарегистрированным пользователям работать с данным декоратором
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # ищем пользователя из базы
        user = User.query.filter_by(username=form.username.data).first()
        # проверяем пароль
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # регистрирум пользователя
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        #
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')  # username - как динамический компонент URL-адреса
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        info = InfoUser(info=current_user, weight=form.weight.data,
                        height=form.height.data,
                        arms=form.arms.data,
                        chest=form.chest.data,
                        waist=form.waist.data,
                        femur=form.femur.data,
                        heartDiseases=form.heartDiseases.data)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('edit_profile'))
        flash('Изменения внесены!')
    # elif request.method == 'GET':
    #     param = current_user.lastinfo_user()
    #     form.femur.data = param.femur
    #     form.waist.data = param.waist
    #     form.weight.data = param.weight
    #     form.height.data = param.height
    #     form.arms.data = param.arms
    #     form.chest.data = param.chest
    #     form.heartDiseases.data = param.heartDiseases

    return render_template('edit_profile.html', title='Edit profile', form=form)


@app.route('/pasport')
@login_required
def pasport():
    param = current_user.information_user()
    return render_template('pasport.html', title='Pasport', param=param)


# @app.route('/select_training', methods =['GET','POST'])
# @login_required
# def select_training():
#     form = SelectTrainingForm()
#
#     if form.validate_on_submit():
#         select_t = Training(tipe=form.tipe.data,
#                             muscle_group=form.muscle_group.data,
#                             name_sport=form.name_sport.data,
#                             gender = current_user.gender)
#         if select_t.tipe == 'no':
#             select_t.tipe = 'Для начинающих'
#         elif select_t.muscle_group == 'no':
#             select_t.muscle_group = 'Все тело'
#         select_t.search_training()
#
#
#     return render_template('select_training.html', title='Подбор тренировки', form = form)




@app.route('/current_training')
@login_required
def current_training():
    u = current_user
    t = Training.query.get(1)
    exercises = t.all_exe()
    return render_template('current_training.html', title='Тренировка', exercises=exercises)
