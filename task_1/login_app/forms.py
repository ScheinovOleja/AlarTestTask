from flask_wtf import FlaskForm
from wtforms import (
    PasswordField, BooleanField, SubmitField, EmailField, StringField, SelectField
)
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField("Ваш Email", validators=[Email()], render_kw={'class': 'input is-large'})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={'class': 'input is-large'})
    remember = BooleanField("Запомнить меня", render_kw={'class': 'checkbox'})
    submit = SubmitField('Войти', render_kw={'class': 'button is-block is-info is-large is-fullwidth'})


class SignupForm(FlaskForm):
    email = EmailField(validators=[Email()], render_kw={'class': 'input is-large', 'placeholder': 'Email'})
    username = StringField(name='username', render_kw={'class': 'input is-large', 'placeholder': 'Имя пользователя'})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={'class': 'input is-large', 'placeholder': 'Пароль'})
    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'button is-block is-info is-large is-fullwidth'})


class ChangeUserForm(FlaskForm):
    username = StringField(name='username', render_kw={'class': 'input is-large', 'placeholder': 'Имя пользователя'})
    email = EmailField(validators=[Email()], name='email',
                       render_kw={'class': 'input is-large', 'placeholder': 'Email'})
    current_password = PasswordField(validators=[DataRequired()], name='cur_pass',
                                     render_kw={'class': 'input is-large', 'placeholder': 'Текущий пароль'})
    password_1 = PasswordField(name='pass1', render_kw={'class': 'input is-large', 'placeholder': 'Пароль'})
    password_2 = PasswordField(name="pass2", render_kw={'class': 'input is-large', 'placeholder': 'Подтвердить пароль'})
    role = SelectField('Addresses', render_kw={'class': 'select'})
    submit = SubmitField('Изменить данные', render_kw={'class': 'button is-block is-info is-large is-fullwidth'},
                         name='save_user')
