# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Connard.Lee
"""

from app.admin.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import traceback

from app.api.schemas import UserSchema
from app.admin.base.models.user import User
from app.extensions import db
from app.api.commons.pagination import paginate


@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')

@blueprint.route('/ui-user-manage')
@login_required
def ui_user_manage():
    try:

        schema = UserSchema(many=True)
        query = User.query
        result = paginate(query, schema)
        template = 'ui-user-manage.html'

        # Detect the current page
        segment = get_segment(request)

        print(result)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        #traceback.print_exc(e)
        return render_template('page-500.html'), 500


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
