from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from login_app.database import db

# class RolesUsers(db.Model):
#     __tablename__ = 'roles_users'
#     __table_args__ = {'extend_existing': True}
#
#     user_id = db.Column(db.Integer())
#     roles_id = db.Column(db.Integer())


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), unique=True),
    db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')),
    extend_existing=True
)


class MyUsers(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    username = db.Column(db.String(50))
    is_superuser = db.Column(db.Boolean())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('user', lazy='dynamic'))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    full_role = db.Column(db.Boolean(False))

    def __str__(self):
        return self.name
