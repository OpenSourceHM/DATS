
import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response, request, current_app
from flask_login import current_user
from app.plugin import async_api
from app.api.schemas import ConfigSchema
from app.api.schemas import ConfigPostSchema
from app.admin.base.models.config import ConfigTable
from app.extensions import db
import traceback

class ConfigResource(Resource):
    """Config resource
    ---
    get:
      description: Get all configure
      tags:
        - Config
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
        - Config
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
        400:
          description: Exception
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
        try:
            # if current_user.role_id != 2:
            #     current_app.logger.info(cfg.to_dict())
            dbdata = {
                'value': json.dumps(request.json['value'])
            }
            cfg = schema.load(dbdata, instance=cfg)
            db.session.commit()

            return {"msg": "config updated", type: schema.dump(cfg)}
        except Exception as e:
            traceback.print_exc(e)
            return {"msg": "Exception", 'e': e}, 400


class ConfigList(Resource):

    """ConfigList resource
    ---
    get:
      tags:
        - Config
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
        - Config
      requestBody:
        content:
          application/json:
            schema:
              ConfigPostSchema
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
                  config: ConfigPostSchema
        400:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: config[key] already exists
                  config: ConfigPostSchema
    """
    method_decorators = [async_api]
    # method_decorators.append(jwt_required())

    async def get(self):
        schema = ConfigSchema(many=True)
        query = ConfigTable.query
        return schema.dump(query)

    async def post(self):

        schema = ConfigPostSchema()
        try:
            dbdata = {
                'key': request.json['key'],
                'value': json.dumps(request.json['value'])
            }
            _config = schema.load(dbdata)

            type = request.json['key']

            # Check config key exists
            exist_user = ConfigTable.query.filter_by(key=_config.key).first()
            if exist_user:
                return {"msg": "config[key] already exists", type: schema.dump(_config)}, 400

            db.session.add(_config)
            db.session.commit()

            return {"msg": "config created", type: schema.dump(_config)}, 201
        except Exception as e:
            return {"msg": "Exception", 'e': e}, 400
