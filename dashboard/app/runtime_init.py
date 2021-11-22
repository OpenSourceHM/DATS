
import uuid
import json
import requests
from flask import request
from app.admin.base.models.user import User, Permissions, Role
from app.admin.base.models.config import ConfigTable

from .version import ver_application, ver_api

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
    network = {
            'port': {
                'web': 80,
                'filebrowser': 8080,
                'nginx': 8081,
                'haproxy': 8082
            },
            'mode': 2,
            'bond': {

                'ifname': "bond9",
                'dhcp': 1,
                'mtu': 1500,
                'mac': "AA:AA:AA:AA:AA:AA",
                'ip': "192.168.20.12",
                'gw': "192.168.20.1",
                'netmask': "255.255.255.0",
            },
            'routes': [
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
                {"target": "192.168.20.1", "mask": "244.255.255.0", "next": "192.168.3.1", "dev": 'et0'}, 
            ],
            'device': [
                {
                    'ifname': "eth0",
                    'dhcp': 1,
                    'mtu': 1500,
                    'ip': "192.168.20.12",
                    'gw': "192.168.20.1",
                    'netmask': "255.255.255.0",
                    'mac': "AA:AA:AA:AA:AA:AA",
                },
                {

                    'ifname': "eth1",
                    'dhcp': 1,
                    'mtu': 1500,
                    'ip': "192.168.20.12",
                    'gw': "192.168.20.1",
                    'netmask': "255.255.255.0",
                    'mac': "AA:AA:AA:AA:AA:AA",
                }
            ],
            'mdns': '192.168.0.100', 
            'sdns': '61.139.2.69',
        }

    item_sys = ConfigTable.query.filter_by(key='system').first()
    if item_sys == None:
        item_sys = ConfigTable(key='system', value=json.dumps(system))
        database.session.add(item_sys)
        database.session.commit()

    item_net = ConfigTable.query.filter_by(key='network').first()
    if item_net == None:
        item_net = ConfigTable(key='network', value=json.dumps(network))
        database.session.add(item_net)
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
        app.logger.critical(json.dumps(tempdata, ensure_ascii=True))
        result = requests.put(url=consul_url, data=json.dumps(
            tempdata, ensure_ascii=True))
        if result.status_code != 200:
            app.logger.info(result.text)
    except :
        pass