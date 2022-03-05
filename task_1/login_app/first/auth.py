from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from login_app import login_manager
from login_app.first.forms import LoginForm, SignupForm
from login_app.database import db
from login_app.first.models import MyUsers, Role

auth = Blueprint('auth', __name__)


@auth.cli.command("createsuperuser")
def create_user():
    username = input('Введите имя пользователя: ')
    email = input('Введите email: ')
    while MyUsers.query.filter_by(email=email).first():
        email = input('Пользователь с таким email уже зарегистрирован! Повторите попытку:')
    password = input('Введите пароль: ')
    new_user = MyUsers(email=email, username=username, password=generate_password_hash(password, method='sha256'),
                       is_superuser=True)
    new_user.roles = [db.session.query(Role).filter(Role.name == 'Админ').first()]
    db.session.add(new_user)
    db.session.commit()
    print('Суперпользователь успешно зарегистрирован!')


@auth.cli.command("init")
def create_user():
    role_1 = Role(name='Админ', description='Полный доступ', full_role=True)
    role_2 = Role(name='Редактор', description='Может редактировать', full_role=False)
    role_3 = Role(name='Пользователь', description='Может смотреть', full_role=False)
    db.session.add_all([role_1, role_2, role_3])
    db.session.commit()
    print('Роли созданы')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@login_manager.user_loader
def load_user(user_id):
    return MyUsers.query.get(int(user_id))


@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(MyUsers).filter(MyUsers.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        flash("Invalid username/password", 'error')
        return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    form = SignupForm()
    return render_template('auth/signup.html', form=form)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = MyUsers.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = MyUsers(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    new_user.roles = [db.session.query(Role).filter(Role.name == 'Пользователь').first()]

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')
