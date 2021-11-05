# -*- encoding: utf-8 -*-
"""
This tool used for flask_babel update translate *.pot *.po *.mo files
Copyright (c) 2021 - present Connard.Lee
"""

import click
import os
from config import Config

@click.group()
def translate():
    """Babel translate plugin cli-tool"""


@translate.command()
def init():
    """Init languages setting in config.py
    """
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    for lang in Config.LANGUAGES:
        if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
@click.argument('lang')
def add(lang):
    """Add a new language

    Support `locale -a` from unix system:

    """
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command("update")
def update():
    """Update all translate files"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('pybabel update failed')
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile *.po to *.mo"""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


if __name__ == "__main__":
    translate()
