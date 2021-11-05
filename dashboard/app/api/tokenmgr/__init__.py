# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Connard.Lee

Token manager is only used for API authentication
"""

from flask import Blueprint

blueprint = Blueprint(
    "tokenmgr_blueprint",
    __name__,
    url_prefix="/api/v1",
    static_folder='static'
)
