# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)
try:
    app.logger.info("Base HTTP Server is available: HTTP/1.1")
    from http.server import BaseHTTPRequestHandler
    BaseHTTPRequestHandler.protocol_version = "HTTP/1.1"
except:
    app.logger.info("Flask work on: HTTP/1.0 as default")

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('HOST        = ' + app_config.HOST)
    app.logger.info('PORT        = ' + app_config.PORT)

if __name__ == "__main__":
    app.run(host=app_config.HOST, port=app_config.PORT)
