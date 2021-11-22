# -*- encoding: utf-8 -*-
'''
 ┌───┐   ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┐
 │Esc│   │ F1│ F2│ F3│ F4│ │ F5│ F6│ F7│ F8│ │ F9│F10│F11│F12│ │P/S│S L│P/B│  ┌┐    ┌┐    ┌┐
 └───┘   └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┘  └┘    └┘    └┘
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐ ┌───┬───┬───┐ ┌───┬───┬───┬───┐
 │~ `│! 1│@ 2│# 3│$ 4│% 5│^ 6│& 7│* 8│( 9│) 0│_ -│+ =│ BacSp │ │Ins│Hom│PUp│ │N L│ / │ * │ - │
 ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤ ├───┼───┼───┤ ├───┼───┼───┼───┤
 │ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{ [│} ]│ | \ │ │Del│End│PDn│ │ 7 │ 8 │ 9 │   │
 ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤ └───┴───┴───┘ ├───┼───┼───┤ + │
 │ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  │               │ 4 │ 5 │ 6 │   │
 ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤     ┌───┐     ├───┼───┼───┼───┤
 │ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│  Shift   │     │ ↑ │     │ 1 │ 2 │ 3 │   │
 ├─────┬──┴─┬─┴──┬┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤ ┌───┼───┼───┐ ├───┴───┼───┤ E││
 │ Ctrl│    │Alt │         Space         │ Alt│    │    │Ctrl│ │ ← │ ↓ │ → │ │   0   │ . │←─┘│
 └─────┴────┴────┴───────────────────────┴────┴────┴────┴────┘ └───┴───┴───┘ └───────┴───┴───┘

Author          : Connard
Github          : https://github.com/lovelacelee
Date            : 2021-11-03 13:54:42
LastEditTime    : 2021-11-22 13:30:38
LastEditors     : Lee
Description     : 
FilePath        : /DATS/dashboard/app/api/routes.py
Copyright 2008-2021 Lovelace, All Rights Reserved.

TODO:
Note:
'''

"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""

from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from app.extensions import apispec

from app.api.resources import UserResource, UserList
from app.api.schemas import UserSchema

from app.api.resources import Check

from app.api.resources import ConfigResource
from app.api.resources import ConfigList

from app.api.resources import ProxyResource, ProxyExtResource
from app.api.resources import ProxyList
from app.api.schemas import ProxySchema, ProxyExtSchema

from app.api import blueprint
api = Api(blueprint)


@blueprint.before_app_first_request
def register_views():
    # USER API
    # --------
    # UserSchema first:
    # lib\site-packages\apispec\ext\marshmallow\__init__.py:208:
    # UserWarning: <class 'app.api.schemas.user.UserSchema'> has already been added to the spec.
    # Adding it twice may cause references to not resolve properly.
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    api.add_resource(UserResource, "/users/<int:user_id>",
                     endpoint="user_by_id")
    api.add_resource(UserList, "/users", endpoint="users")
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    # Check
    # --------
    api.add_resource(Check, "/check/<string:type>", endpoint="check")
    apispec.spec.path(view=Check, app=current_app)

    # Config API
    # --------
    api.add_resource(ConfigResource, '/config/<string:type>',
                     endpoint="config")
    api.add_resource(ConfigList, '/config', endpoint="configlist")
    apispec.spec.path(view=ConfigResource, app=current_app)
    apispec.spec.path(view=ConfigList, app=current_app)
    # Proxy API
    # --------
    apispec.spec.components.schema("ProxySchema", schema=ProxySchema)
    api.add_resource(ProxyResource, "/proxy/<int:proxy_id>",
                     endpoint="proxy_by_id")
    api.add_resource(ProxyList, "/proxy", endpoint="proxy")
    apispec.spec.path(view=ProxyResource, app=current_app)
    apispec.spec.path(view=ProxyList, app=current_app)

    apispec.spec.components.schema("ProxyExtSchema", schema=ProxyExtSchema)
    api.add_resource(ProxyExtResource, "/proxy/<string:remote_addr>/<int:remote_port>",
                     endpoint="proxy_by_detail")
    apispec.spec.path(view=ProxyExtResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
