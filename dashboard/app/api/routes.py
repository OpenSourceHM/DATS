# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Connard.Lee
"""

from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from app.extensions import apispec

from app.api.resources import UserResource, UserList
from app.api.schemas import UserSchema
from app.api.resources import ImgProxy

from app.api import blueprint
api = Api(blueprint)

@blueprint.before_app_first_request
def register_views():
    # USER API
    # --------
    # api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
    # api.add_resource(UserList, "/users", endpoint="users")
    # apispec.spec.path(view=UserResource, app=current_app)
    # apispec.spec.path(view=UserList, app=current_app)
    # apispec.spec.components.schema("UserSchema", schema=UserSchema)
    # CNBING
    # --------
    api.add_resource(ImgProxy, "/background/<int:idx>/<int:n>", endpoint="background")
    apispec.spec.path(view=ImgProxy, app=current_app)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
