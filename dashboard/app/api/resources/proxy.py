
import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response, request, current_app
from app.plugin import async_api
from app.api.resources._freeport import FreePort
from app.api.schemas import ProxySchema, ProxyExtSchema

from app.admin.base.models.proxy import ProxyTable
from app.extensions import db
from app.api.commons.pagination import paginate

# For web ui


class ProxyResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - Proxy
      parameters:
        - in: path
          name: proxy_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  proxy: ProxySchema
        404:
          description: proxy does not exists
    put:
      tags:
        - Proxy
      parameters:
        - in: path
          name: proxy_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              ProxySchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy updated
                  proxy: ProxySchema
        404:
          description: proxy does not exists
    delete:
      tags:
        - Proxy
      parameters:
        - in: path
          name: proxy_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy deleted
        404:
          description: proxy does not exists
    """

    # method_decorators = [jwt_required()]

    def get(self, proxy_id):
        schema = ProxySchema()
        proxy = ProxyTable.query.get_or_404(proxy_id)
        return {"proxy": schema.dump(proxy)}

    def put(self, proxy_id):
        schema = ProxySchema(partial=True)
        proxy = ProxyTable.query.get_or_404(proxy_id)
        proxy = schema.load(request.json, instance=proxy)

        db.session.commit()

        return {"msg": "proxy updated", "proxy": schema.dump(proxy)}

    def delete(self, proxy_id):
        proxy = ProxyTable.query.get_or_404(proxy_id)
        db.session.delete(proxy)
        db.session.commit()

        return {"msg": "proxy deleted"}

# For DAGMS


class ProxyExtResource(Resource):
    """Single object resource

    ---
    put:
      tags:
        - Proxy
      parameters:
        - name: remote_addr
          in: path
          schema:
            type: string
          examples:
            192.168.20.121:
              summary: Proxy remote address
              value: 192.168.20.121
        - name: remote_port
          in: path
          schema:
            type: number
          examples:
            80: 
              summary: Proxy remote port
              value: 80
      requestBody:
        content:
          application/json:
            schema:
              ProxyExtSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy updated
                  proxy: ProxyExtSchema
        404:
          description: proxy does not exists
    delete:
      tags:
        - Proxy
      parameters:
        - name: remote_addr
          in: path
          schema:
            type: string
          examples:
            192.168.20.121:
              summary: Proxy remote address
              value: 192.168.20.121
        - name: remote_port
          in: path
          schema:
            type: number
          examples:
            80: 
              summary: Proxy remote port
              value: 80
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy deleted
        404:
          description: proxy does not exists
    """

    # method_decorators = [jwt_required()]

    def put(self, remote_addr, remote_port):
        schema = ProxySchema(partial=True)
        try:
            proxy = ProxyTable.query.filter_by(
                remote_addr=remote_addr, remote_port=remote_port).first()
            if proxy:
                proxy = schema.load(request.json, instance=proxy)

                db.session.commit()

                return {"msg": "proxy updated", "proxy": schema.dump(proxy)}
        except Exception as e:
            return {"msg": "Exception", 'e': e}, 400

    def delete(self, remote_addr, remote_port):
        try:
            proxy = ProxyTable.query.filter_by(
                remote_addr=remote_addr, remote_port=remote_port).first()

            if proxy:

                current_app.logger.info(proxy)
                db.session.delete(proxy)
                db.session.commit()

                return {"msg": "proxy deleted"}
            else:
                return {"msg": "proxy not exists"}, 200
        except Exception as e:
            return {"msg": "Exception", 'e': e}, 400

# For both


class ProxyList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - Proxy
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/ProxySchema'
    post:
      tags:
        - Proxy
      requestBody:
        content:
          application/json:
            schema:
              ProxySchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy created
                  proxy: ProxySchema
        400:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: listen_port already exists
                  proxy: ProxySchema

    delete:
      tags:
        - Proxy
      requestBody:
        content:
          application/json:
            schema:
              ProxySchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: proxy deleted
        400:
          description: proxy delete error
    """

    # method_decorators = [jwt_required()]

    def get(self):
        schema = ProxySchema(many=True)
        query = ProxyTable.query
        return paginate(query, schema)

    def post(self):
        schema = ProxySchema()
        print(request.json)

        if 'listen_port' in request.json:
          # Check exists
          exist_proxy = ProxyTable.query.filter_by(
              remote_addr=proxy.remote_addr, remote_port=proxy.remote_port).first()

          if exist_proxy:
              return {"msg": "proxy relationship already exists", "proxy": schema.dump(exist_proxy)}, 200
          exist_listen_port = ProxyTable.query.filter_by(
              listen_port=proxy.listen_port).first()
          if proxy.listen_port > 0 and exist_listen_port:
              return {"msg": "listen_port already exists", "proxy": schema.dump(exist_listen_port)}, 400
          FP = FreePort(10000, 30000)
          if proxy.listen_port == 0:
            proxy.listen_port = FP.port
          db.session.add(proxy)
          db.session.commit()

          return {"msg": "proxy created", "proxy": schema.dump(proxy)}, 201
        else:
          FP = FreePort(10000, 30000)
          request.json['listen_port'] = FP.port
          proxy = schema.load(request.json)

          db.session.add(proxy)
          db.session.commit()

          return {"msg": "proxy created", "proxy": schema.dump(proxy)}, 201

    def delete(self):

        try:
            proxy = ProxyTable.query.filter_by(
                remote_addr=request.json['remote_addr'], remote_port=request.json['remote_port']).first()

            if proxy:

                current_app.logger.info(proxy)
                db.session.delete(proxy)
                db.session.commit()

                return {"msg": "proxy deleted"}
            else:
                return {"msg": "proxy not exists"}, 200
        except Exception as e:
            return {"msg": "Exception", 'e': e}, 400
