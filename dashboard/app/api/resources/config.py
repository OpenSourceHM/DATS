
import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response, request, current_app
from app.plugin import async_api
from app.api.schemas import ConfigSchema
from app.admin.base.models.config import ConfigTable
from app.extensions import db


class ConfigResource(Resource):
    """Config resource
    ---
    get:
      description: Get all configure
      tags:
        - api
      parameters:
        - name: type
          in: path
          schema:
            type: string
          examples:
            system:
              summary: system parameters
              value: system
            network:
              summary: network parameters
              value: network

      responses:
        200:
          description: request successfully
          content:
            application/json:
              schema:
                properties:
                  result:
                    decription: result
                    type: object
        400:
          description: Some error occurred

    put:
      tags:
        - api
      parameters:
        - in: path
          name: type
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              ConfigSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: config updated
                  cfg: ConfigSchema
        404:
          description: config does not exists
    """
    method_decorators = [async_api]
    # method_decorators.append(jwt_required())

    async def get(self, type):
        schema = ConfigSchema()
        cfg = ConfigTable.query.filter_by(key=type).first_or_404()
        return {type: schema.dump(cfg)}

    async def put(self, type):
        schema = ConfigSchema(partial=True)
        cfg = ConfigTable.query.filter_by(key=type).first_or_404()
        cfg = schema.load(request.json, instance=cfg)
        db.session.commit()

        return {"msg": "config updated", type: schema.dump(cfg)}


class ConfigList(Resource):

    """ConfigList resource
    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      results:
                        type: array
    
    post:
      description: Post new configure
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              ConfigSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: config created
                  config: ConfigSchema
        400:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: config[key] already exists
                  config: ConfigSchema
    """
    method_decorators = [async_api]
    # method_decorators.append(jwt_required())
    

    def get(self):
        schema = ConfigSchema(many=True)
        query = ConfigTable.query
        return schema.dump(query)

    async def post(self):
        current_app.logger.info(request.json)
        schema = ConfigSchema()
        _config = schema.load(request.json)
        current_app.logger.info(_config)
        type = _config['key']
        current_app.logger.info(_config)

        # Check config key exists
        exist_user = ConfigTable.query.filter_by(key=_config.key).first()
        if exist_user:
            return {"msg": "config[key] already exists", type: schema.dump(_config)}, 400

        db.session.add(_config)
        db.session.commit()

        return {"msg": "config created", type: schema.dump(_config)}, 201