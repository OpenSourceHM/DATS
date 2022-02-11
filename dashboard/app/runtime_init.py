
import uuid
import json
import requests
import threading
import time
from flask import request
from app.admin.base.models.user import User, Permissions, Role
from app.admin.base.models.config import ConfigTable

from .version import ver_application, ver_api
from .plugin import netdev

def user_init(app, database):

    exist = User.query.filter_by(username='admin').all()
    admin = User.query.filter_by(username='admin').first()

    if len(exist) == 0 or admin == None:
        user = User(username="admin", email="lovelacelee@gmail.com",
                    password="admin", active=True, role_id=Permissions.ADMINISTRATOR)
        database.session.add(user)
        database.session.commit()
        app.logger.info("created user admin")
    Role.init_role()


def config_init(app, database):
    system = {
        'sn': str(uuid.uuid4()),
        'name': u'数据接入服务',
        'address': u'成都市武侯区天华二路219号',
        'latitude': '104.078133',
        'longitude': '30.54587'
    }
    item_sys = ConfigTable.query.filter_by(key='system').first()
    if item_sys == None:
        item_sys = ConfigTable(key='system', value=json.dumps(system))
        database.session.add(item_sys)
        database.session.commit()
    # listen_port
    listen_port = {
        'web': 80,
        'filebrowser': 8080,
        'nginx': 8081,
        'haproxy': 8082
    }
    item_listen_port = ConfigTable.query.filter_by(key='listen_port').first()
    if item_listen_port == None:
        item_listen_port = ConfigTable(
            key='listen_port', value=json.dumps(listen_port))
        database.session.add(item_listen_port)
        database.session.commit()
    # mode and dns
    network = {
        'mdns': '192.168.0.100',
        'sdns': '61.139.2.69',
    }

    item_net = ConfigTable.query.filter_by(key='network').first()
    if item_net == None:
        item_net = ConfigTable(key='network', value=json.dumps(network))
        database.session.add(item_net)
        database.session.commit()

    # Network device
    nd = netdev()
    for iname in range(nd.count):
        iname_key = "ndev_"+str(iname)
        item_ndev = ConfigTable.query.filter_by(key=iname_key).first()

        if item_ndev == None:
            item_ndev = ConfigTable(
                key=iname_key, value=json.dumps({
                    'ifname': "eth"+str(iname),
                    'dhcp': 1,
                    'mtu': 1500,
                    'ip': "192.168.20.135",
                    'gw': "192.168.20.1",
                    'netmask': "255.255.255.0",
                    'mac': "AA:AA:AA:AA:AA:AA",
                }))
            database.session.add(item_ndev)
            database.session.commit()
    # Consul
    consul = {
        'ip': '192.168.0.59',
        'port': 8500,
        'api': '/v1/agent/service/register',
    }
    item_consul = ConfigTable.query.filter_by(key='consul').first()
    if item_consul == None:
        item_consul = ConfigTable(key='consul', value=json.dumps(consul))
        database.session.add(item_consul)
        database.session.commit()

    return item_sys


def register_consul(app):

    # TODO: Call consul API
    consul = {
        'ip': "192.168.20.121",
        'port': '8500',
        'api': '/v1/agent/service/register'
    }
    consul_url = 'http://'+consul['ip']+':'+consul['port']+consul['api']
    app.logger.info('Register to consul service:'+consul_url)
    tempdata = {
        'id': 'test',  # show in consul ui
        'name': 'DATS',
        'address': '192.168.20.121',
        'port': 5000,
        'tags': [
            'ver_application:'+ver_application,
            'ver_api:'+ver_api
        ],
        'meta': {
            'id': 'did',
            'name': 'DATS-aaa'
        },
        'checks': [
            {
                'http': 'http://192.168.20.121:5000/api/v1/check/consul',
                'interval': '10s'
            }
        ]
    }
    try:
        app.logger.info(json.dumps(tempdata, ensure_ascii=True))
        result = requests.put(url=consul_url, data=json.dumps(
            tempdata, ensure_ascii=True))
        if result.status_code != 200:
            app.logger.error(result.text)
    except Exception as e:
        app.logger.critical(e)

def server_monitor(app):
    while True:
        time.sleep(10)
        register_consul(app)

def server_init(app):
    return
    t = threading.Thread(target=server_monitor, args=(app,), name="server_monitor")
    t.start()