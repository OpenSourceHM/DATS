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

from app.api.schemas import UserSchema
from app.admin.base.models.user import User, Role, Permissions
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

        print(current_user)

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
        # TODO: query system settings
        result = {
            'name': 'Test',
            'address': 'Test adres',
            'sn': '12346546464',

            'latitude': '2323.232323',
            'longitude': '2323423.234234234',
        }
        template = 'system.html'

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


@blueprint.route('/network')
@login_required
def network_settings():
    try:
        # TODO: query network settings
        result = {
            'port': {
                'web': 80,
                'filebrowser': 8080,
                'nginx': 8081,
                'haproxy': 8082
            },
            'mode': 2,
            'bond': {

                'ifname': "bond9",
                'dhcp': 1,
                'mtu': 1500,
                'mac': "AA:AA:AA:AA:AA:AA",
                'ip': "192.168.20.12",
                'gw': "192.168.20.1",
                'netmask': "255.255.255.0",
            },
            'routes': [
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
            ],
            'device': [
                {
                    'ifname': "eth0",
                    'dhcp': 1,
                    'mtu': 1500,
                    'ip': "192.168.20.12",
                    'gw': "192.168.20.1",
                    'netmask': "255.255.255.0",
                    'mac': "AA:AA:AA:AA:AA:AA",
                },
                {

                    'ifname': "eth1",
                    'dhcp': 1,
                    'mtu': 1500,
                    'ip': "192.168.20.12",
                    'gw': "192.168.20.1",
                    'netmask': "255.255.255.0",
                    'mac': "AA:AA:AA:AA:AA:AA",
                }
            ],
            'mdns': '192.168.0.100', 
            'sdns': '61.139.2.69',
        }
        template = 'network.html'

        # Detect the current page
        segment = get_segment(request)

        print(current_user)

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
        result = []
        template = 'app-tcp.html'

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
