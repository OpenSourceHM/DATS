# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""

from app.admin.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import traceback
import json
from app.plugin import netifaces
from app.plugin import netdev
from app.api.schemas import UserSchema
from app.api.schemas import ConfigSchema
from app.api.schemas import ProxySchema
from app.admin.base.models.user import User, Role, Permissions
from app.admin.base.models.config import ConfigTable
from app.admin.base.models.proxy import ProxyTable
from app.extensions import db
from app.api.commons.pagination import paginate
from app.permission_required import permission_required

from flask_babel import _
from flask_babel import lazy_gettext as _l


@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/users')
@permission_required(Permissions.ADMINISTRATOR)
@login_required
def users_manage():
    try:

        schema = UserSchema(many=True)
        query = User.query
        result = paginate(query, schema)
        template = 'users.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        # traceback.print_exc(e)
        return render_template('page-500.html'), 500


@blueprint.route('/system')
@login_required
def system_settings():
    try:

        # schema = ConfigSchema()
        query = ConfigTable.query.filter_by(key='system').first()
        consul = ConfigTable.query.filter_by(key='consul').first()

        result = json.loads(query.value)
        result['consul'] = json.loads(consul.value)
        template = 'system.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        # traceback.print_exc(e)
        return render_template('page-500.html'), 500


@blueprint.route('/network')
@login_required
def network_settings():
    try:

        # schema = ConfigSchema()
        network = ConfigTable.query.filter_by(key='network').first()
        result = json.loads(network.value)
        try:
            devices = result['devices']
        except:
            pass
        listen_port = ConfigTable.query.filter_by(key='listen_port').first()
        result['listen_port'] = json.loads(listen_port.value)
        nd = netdev()
        nd.init()

        result['devices'] = []
        for i in range(nd.count):
            devinfo = nd.devinfo[i]
            try:
                devinfo['dhcp'] = devices[i]['dhcp']
                devinfo['addr'] = devices[i]['addr']
                devinfo['gateway'] = devices[i]['gateway']
                devinfo['netmask'] = devices[i]['netmask']
            except Exception as e:
                pass
            result['devices'].append({
                'id': i,
                'value': devinfo
            })
        
        result['routes'] = nd.gw
        print(result)
        template = 'network.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        traceback.print_exc(e)
        return render_template('page-500.html'), 500


@blueprint.route('/app-tcp')
@login_required
def app_tcp():
    try:

        schema = ProxySchema(many=True)
        query = ProxyTable.query
        result = paginate(query, schema)
        template = 'app-tcp.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        # traceback.print_exc(e)
        return render_template('page-500.html'), 500


@blueprint.route('/app-http')
@login_required
def app_http():
    try:
        result = []
        template = 'app-http.html'

        # Detect the current page
        segment = get_segment(request)

        print(current_user)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment, data=result)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        # traceback.print_exc(e)
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
