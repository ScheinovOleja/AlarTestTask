import json

from flask import Blueprint, render_template, redirect, url_for
from flask import request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from login_app import db
from login_app.forms import ChangeUserForm
from login_app.models import Role, MyUsers

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    """
    Рендер главной страницы. Доступна только "залогинившимся" пользователям.
    :return:
    """
    # Если пользователь не вошел в систему, редирект на страницу "логина"
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    all_user = MyUsers.query.all()
    return render_template('index.html', all_users=all_user)


@main.route('/delete_user', methods=["POST"])
@login_required
def change_user_post_delete():
    """
    Удаление пользователя из базы данных. Вход через AJAX.
    :return:
    """
    # "Защита" от отправки сигналов из postman и прочих вещей, чтобы пользователей не мог удалить кто угодно.
    if current_user.roles[0].name == 'Админ' or current_user.roles[0].name == 'Редактор':
        data = request.json
        user = MyUsers.query.get(int(data['id']))
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'msg': 'Пользователь успешно удален!'})
    else:
        return json.dumps({'msg': 'А кто это тут пытается у меня пользователей удалить, а?)))'})


@main.route('/change_user', methods=["POST"])
@login_required
def change_user_post_change():
    """
    Редактирование пользователей. Вход из AJAX
    :return:
    """
    data = request.json
    user = MyUsers.query.get(int(data['id']))
    user.username = data['username']
    user.email = data['email']
    user.roles[0] = (Role.query.get(int(data['role'])))
    # если пароль введен, проверка валидности пароля для замены
    if data['cur_pass']:
        if data['pass1'] == data['pass2']:
            # Если текущий пароль введен верно, смена пароля на новый
            if user.check_password(data['cur_pass']):
                user.password = generate_password_hash(data['pass1'])
            else:
                return json.dumps({'msg': 'Неверно указан текущий пароль!'})
        else:
            return json.dumps({'msg': 'Пароли не совпадают!'})
    db.session.add(user)
    db.session.commit()
    return json.dumps({'msg': 'Данные успешно изменены!'})


@main.route('/change_user/<int:pk>', methods=["GET"])
@login_required
def change_user_get_change(pk):
    """
    Рендер страницы редактирования пользователя
    :param pk:
    :return:
    """
    form = ChangeUserForm()
    user = MyUsers.query.get(int(pk))
    form.username.render_kw['value'] = user.username
    form.email.render_kw['value'] = user.email
    form.submit.render_kw['data-id'] = user.id
    all_roles = Role.query.all()
    # Я вообще не знаю, как сделать в Select значение по умолчанию тут, поэтому колесо из сапог 😃
    try:
        form.role.choices = [(user.roles[0].id, user.roles[0])]
        for role in all_roles:
            if role.id != user.roles[0].id:
                form.role.choices.append((role.id, role))
    except IndexError:
        # Обезопасил момент, когда у пользователя нет никакой роли(по умолчанию новые пользователи получают
        # роль "пользователь")
        form.role.choices = [('-', '-')]
        for role in all_roles:
            form.role.choices.append((role.id, role))
    return render_template('change_user.html', user=user, form=form)


@main.route('/change_role', methods=['GET'])
def get_roles():
    """
    Рендер страницы со списком всех ролей. Доступно только суперпользователю.
    :return:
    """
    all_roles = Role.query.all()
    if not current_user.is_superuser:
        return redirect(url_for('main.index'))
    return render_template('get_roles.html', roles=all_roles)
