# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Connard.Lee
"""

from flask import jsonify, render_template, redirect, request, url_for, current_app
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

import time
from app.extensions import pwd_context, jwt, apispec
from app import db, login_manager
from app.admin.base import blueprint
from app.admin.base.forms import LoginForm, CreateAccountForm
from app.admin.base.models.user import User, Role, Permissions

from app.admin.base.util import verify_pass
from flask_babel import _
from flask_babel import lazy_gettext as _l


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        # if user and verify_pass( password, user.password):
        if user and pwd_context.verify(password, user.password):
            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html', msg=_('Wrong user or password'), form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg=_('Username already registered'),
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg=_('Email already registered'),
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg=_(
                                   'User created please <a href="/login">login</a>'),
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form,
                               segment='register')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500