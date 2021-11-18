"""DATS proxy table
"""
from app.extensions import db
import json

class ProxyTable(db.Model):

    __tablename__ = 'Proxy'

    id = db.Column(db.Integer, primary_key=True)
    # Proxy nickname
    proxy_name = db.Column(db.String(64), nullable=False, default="")
    # Local listen port, Unique
    listen_port = db.Column(db.Integer, nullable=False, unique=True, default=9000)
    # Remote address, ip or domain
    remote_addr = db.Column(db.String, nullable=False)
    # Remote listen port
    remote_port = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "proxy_name": self.proxy_name,
            "remote_addr": self.remote_addr,
            "remote_port": self.remote_port,
            "listen_port": self.listen_port
        }
