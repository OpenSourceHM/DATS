
import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response
from app.plugin import async_api


class Check(Resource):
    """Check resource
    ---
    get:
      description: Status check API
      tags:
        - Check
      parameters:
        - name: type
          in: path
          schema:
            type: string
          examples:
            health:
              summary: health check callback
              value: consul

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

    """
    method_decorators = [async_api]

    async def get(self, type):
        try:
            statusCode = 200
            if type == 'consul':
                data = {
                    'type': type,
                    'health': "OK"
                }
            else:
                statusCode = 400
                data = {
                    'type': type,
                    'health': "Unsupported"
                }
            return Response(json.dumps(data, default=lambda object: object.__dict__, sort_keys=True, indent=4),
                            status=statusCode,
                            mimetype='application/json')
        except Exception as e:
            data = {
                "result": str(e)
            }
            return Response(json.dumps(data, default=lambda object: object.__dict__, sort_keys=True, indent=4),
                            status=400,
                            mimetype='application/json')
