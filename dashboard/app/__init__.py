# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""


from flask import Flask, url_for, request
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask import Blueprint
from app.extensions import apispec
from app.extensions import db
from app.extensions import jwt
from app.extensions import migrate
from app.extensions import babel
from app.extensions import login_manager
from app.plugin import cors_init_app

from app.runtime_init import user_init
from app.runtime_init import config_init
from app.runtime_init import register_consul

def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


def register_blueprints(app):
    # admin
    for module_name in ('base', 'home'):
        module = import_module('app.admin.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
    # api
    app.register_blueprint(import_module('app.api.routes').blueprint)
    app.register_blueprint(import_module('app.api.tokenmgr.routes').blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()
        try:
            user_init(app, db)
            config_init(app, db)
        except Exception as e:
            app.logger.critical(e)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    # static_url_path Only set the vhost url, static_folder set the real source filepath
    app = Flask(__name__, static_url_path='/admin/static',
                static_folder='admin/base/static')
    app.config.from_object(config)
    cors_init_app(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_apispec(app)

    register_consul(app)
    return app
