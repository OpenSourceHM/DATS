# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Connard.Lee
"""

from flask import Blueprint

blueprint = Blueprint(
    "api_blueprint",
    __name__,
    url_prefix="/api/v1"
)
