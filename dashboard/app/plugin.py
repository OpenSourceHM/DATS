# -*- encoding: utf-8 -*-
'''
Copyright 2021 Connard Lee

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from flask_cors import CORS
import asyncio
import json
import requests
from functools import wraps
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from flask import has_request_context
from flask import copy_current_request_context
from flask import current_app, request, jsonify
from app.extensions import babel
from .version import did
"""
Flask CORS issue
"""

"""
app: flask app
"""


def cors_init_app(app):
    # Global CORS
    CORS(app, supports_credentials=True)


def async_api(func):
    """
    Aysnc API wrapper
    Usage:
        @app.route('/the/api/route')
        @cross_origin()
        @async_api
        async def api():
            return something
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        call_result = Future()

        def _run():
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
            except Exception as error:
                call_result.set_exception(error)
            else:
                call_result.set_result(result)
            finally:
                loop.close()

        loop_executor = ThreadPoolExecutor(max_workers=1)
        if has_request_context():
            _run = copy_current_request_context(_run)
        loop_future = loop_executor.submit(_run)
        loop_future.result()

        """
        FIXME: ThreadPoolExecutor cannot exit while Exception occurred
        """
        return call_result.result()

    return _wrapper


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'zh'


def register_consul(app):
    # TODO: read config from database
    # TODO: Call consul API
    consul = {
        'ip': "192.168.20.121",
        'port': '8500',
        'api': '/v1/agent/service/register'
    }
    consul_url = 'http://'+consul['ip']+':'+consul['port']+consul['api']
    app.logger.info('Register to consul service:'+consul_url)
    tempdata = {
        'id': did,  # show in consul ui
        'name': 'DATS',
        'address': '192.168.20.121',
        'port': 5000,
        'tags': ['dev'],
        'meta': {
            'id': did,
            'name': 'DATS-aaa'
        },
        'checks': [
            {
                'http': 'http://192.168.20.121:5000/api/v1/check/consul',
                'interval': '1s'
            }
        ]
    }
    app.logger.critical(json.dumps(tempdata, ensure_ascii=True))
    result = requests.put(url=consul_url, data=json.dumps(
        tempdata, ensure_ascii=True))
    if result.status_code != 200:
        app.logger.info(result.text)
