
import random
import socket
from app.admin.base.models.proxy import ProxyTable


class FreePort(object):
    """Get a free port from system

    Step 1: Generate a random port number

    Step 2: Check if it's already exists in database
    """

    def __init__(self, start, stop):
        self.port = None
        self.sock = socket.socket()

        port = start
        while True:
            try:
                # Check exists
                exist_proxy = ProxyTable.query.filter_by(
                    listen_port=port).first()
                if exist_proxy:
                    port = port + 1
                    continue
                self.sock.bind(('', port))
                self.port = port
                break
            except Exception:
                port = port + 1
                continue
        self.sock.close()

