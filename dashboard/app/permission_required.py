# coding:utf-8

from functools import wraps
from flask import session, render_template
from app.extensions import db
from app.admin.base.models.user import User, Role

Permission_code = [0X01, 0X02]


def permission_can(current_user, permission):
    """
    :param current_user
    :param permission
    :return:
    """
    print("@#" * 10)
    role_id = current_user.role_id
    print("#" * 120)
    print(role_id)
    role = db.session.query(Role).filter_by(id=role_id).first()
    return (role.permissions & permission) == permission


def permission_required(permission):
    """
    :param permission:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                flag = False
                current_user = User.query.filter_by(
                    id=session.get('user_id')).first()
                if current_user:
                    role_id = current_user.role_id
                    role = db.session.query(Role).filter_by(id=role_id).first()
                    if role.permissions & permission == permission:
                        flag = True
                if flag:
                    return f(*args, **kwargs)
                else:
                    return render_template('page-403.html'), 403
            except:
                return render_template('page-403.html'), 403
        return decorated_function
    return decorator
