# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String

from app import login_manager

from app.admin.base.util import hash_pass
# --
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db, pwd_context

# JWT password mode
# class User(db.Model):
#     """Basic user model"""

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     _password = db.Column("password", db.String(255), nullable=False)
#     active = db.Column(db.Boolean, default=True)

#     @hybrid_property
#     def password(self):
#         return self._password

#     @password.setter
#     def password(self, value):
#         self._password = pwd_context.hash(value)

#     def __repr__(self):
#         return "<User %s>" % self.username


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    # Simple password use Binary
    #password = Column(Binary)
    _password = db.Column("bak_password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            # Simple password mode
            # if property == 'password':
            #     value = hash_pass( value ) # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Permissions:
    """
    """
    USERGROUP = 0X01
    ADMINISTRATOR = 0X02


class Role(db.Model):
    """
    User Role
    """
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def init_role():
        role_name_list = ['user', 'admin']
        roles_permission_map = {
            'user': [Permissions.USERGROUP],
            'admin': [Permissions.ADMINISTRATOR, Permissions.USERGROUP]
        }
        try:
            for role_name in role_name_list:
                role = Role.query.filter_by(name=role_name).first()
                if role is None:
                    role = Role(name=role_name)
                role.reset_permissions()
                for permission in roles_permission_map[role_name]:
                    role.add_permission(permission)
                db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return self.permissions & permission == permission

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions |= permission
