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
from functools import wraps
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from flask import has_request_context
from flask import copy_current_request_context
from flask import current_app, request, jsonify
from sqlalchemy import null
from app.extensions import babel
import netifaces
import platform
import uuid
import socket
import psutil
import traceback

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

class netdev:
    def __init__(self):
        self.count = 0
        self.devinfo = []
        self.gw = []
        self.hostname = socket.gethostname()

    def init(self):
        self.gw = self.gateway()
        self._devices = netifaces.interfaces()
        for i in self._devices:
            devinfo = None
            try:
                devinfo = self.ifaddr(i)[netifaces.AF_INET][0]
            except Exception as e:
                pass
            finally:
                if devinfo is not None and devinfo['addr'] != '127.0.0.1':
                    adapter = self.mac_from_ip(devinfo['addr'])
                    devinfo['ifname'] = adapter[0]
                    devinfo['mac'] = adapter[1]
                    devinfo['gateway'] = self.gateway_ip(i, adapter[0])
                    self.devinfo.append(devinfo)
        self.count = len(self.devinfo)

    def mac_from_ip(self, ipv4, ipv6 = None):
        dic = psutil.net_if_addrs()
        for adapter in dic:
            snicList = dic[adapter]
            ifname = adapter
            mac = None
            _ipv4 = None
            _ipv6 = None
            for snic in snicList:
                if snic.family.name in {'AF_LINK', 'AF_PACKET'}:
                    mac = snic.address
                elif snic.family.name == 'AF_INET':
                    _ipv4 = snic.address
                elif snic.family.name == 'AF_INET6':
                    _ipv6 = snic.address
            if _ipv4 == ipv4:
                return ifname, mac

        return None

    def gateway_ip(self, ifname, nic):
        for i in self.gw:
            if i[1] == ifname:
                i.append(nic)
                return i[0]
    
    def get_mac_address(self):
        """Only support single network device"""
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
        return "-".join([mac[e:e+2] for e in range(0,11,2)])

    def gateway(self):
        """Get gateway

        Returns:
            list
        """
        gw = []
        try:
            for g in netifaces.gateways()[netifaces.AF_INET]:
                gw.append(list(g))

        except Exception as e:
            #traceback.print_exc(e)
            pass
        finally:
            return gw

    def ifaddr(self, i):
        return netifaces.ifaddresses(i)
        