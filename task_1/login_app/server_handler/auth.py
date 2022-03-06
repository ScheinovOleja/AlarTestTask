from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from login_app import login_manager
from login_app.forms import LoginForm, SignupForm
from login_app.models import MyUsers, Role, db

auth = Blueprint('auth', __name__)


@auth.cli.command("createsuperuser")
def create_user():
    """
    Консольная команда Flask для создания суперпользователя. Используется в init.sh
    :return:
    """
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
    """
    Консольная команда для создания ролей пользователей для разграничения их прав. Используется в init.sh
    :return:
    """
    role_1 = Role(name='Админ', description='Полный доступ', full_role=True)
    role_2 = Role(name='Редактор', description='Может редактировать', full_role=False)
    role_3 = Role(name='Пользователь', description='Может смотреть', full_role=False)
    db.session.add_all([role_1, role_2, role_3])
    db.session.commit()
    print('Роли созданы')


@login_manager.user_loader
def load_user(user_id):
    """
    Функция для "загрузки" пользователя в сессию при каждом обращении на сервер.
    :param user_id:
    :return:
    """
    return MyUsers.query.get(int(user_id))


@auth.route('/login', methods=['GET'])
def login():
    """
    Рендер страницы "логина"
    :return:
    """
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    """
    Проверка правильности введенных данных и дальнейшее перенаправление пользователя.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Проверка существования пользователя
        user = db.session.query(MyUsers).filter(MyUsers.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            # Если пользователь существует и пароль введен верно, вход и редирект на главную страницу
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        # Если неверно, вывод сообщения об ошибке и редирект на страницу "логина"
        flash("Неверное имя пользователя/пароль!", 'error')
        return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET'])
def signup():
    """
    Рендер страницы регистрации.
    :return:
    """
    form = SignupForm()
    return render_template('auth/signup.html', form=form)


@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Регистрация нового пользователя.
    :return:
    """
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = MyUsers.query.filter_by(email=email).first()  # проверка существования в БД пользователя с таким же email

    if user:  # если пользователь найден, вывод ошибки и редирект на страницу регистрации
        flash('Данный email уже зарегистрирован!')
        return redirect(url_for('auth.signup'))

    # Создание нового пользователя
    new_user = MyUsers(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    # Назначение пользователю роли "пользователь"
    new_user.roles = [db.session.query(Role).filter(Role.name == 'Пользователь').first()]

    # Добавление пользователя в БД и сохранение БД
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    """
    Выход пользователя из сессии.
    :return:
    """
    logout_user()
    return redirect('login')
