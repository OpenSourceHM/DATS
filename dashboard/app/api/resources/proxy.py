
import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response, request, current_app
from app.plugin import async_api
from app.api.schemas import ProxySchema

from app.admin.base.models.proxy import ProxyTable
from app.extensions import db
from app.api.commons.pagination import paginate


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
        proxy = schema.load(request.json)

        # Check listen_port exists
        exist_proxy = ProxyTable.query.filter_by(
            listen_port=proxy.listen_port).first()
        if exist_proxy:
            return {"msg": "listen_port already exists", "proxy": schema.dump(proxy)}, 400

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
