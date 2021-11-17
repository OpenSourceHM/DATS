# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present cong.li@huamaitel.com
"""

from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static'
)
