
import json
import requests
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import Response
from app.plugin import async_api

# Proxy of
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=3


class ImgProxy(Resource):
    """ImgProxy resource
    ---
    get:
      description: get images form cn.bing.com
      tags:
        - api
      parameters:
        - name: idx
          in: path
          schema:
            type: number
          examples:
            0:
              summary: index of image list
              value: 0
        - name: n
          in: path
          schema:
            type: number
          examples:
            8: 
              summary: number of image list[0~8]
              value: 8

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
    # method_decorators = [async_api, jwt_required()]

    async def get(self, idx, n):
        try:
            url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx={}&n={}".format(
                idx, n)
            result = requests.get(url)
            json_result = json.loads(result.text)
            data = []
            for i in json_result['images']:
                data.append({
                    'url': '{}/{}'.format('https://cn.bing.com', i['url']),
                    'startdate': i['startdate'],
                    'enddate': i['enddate'],
                    'title': i['copyright']
                })
            return Response(json.dumps(data, default=lambda object: object.__dict__, sort_keys=True, indent=4),
                            mimetype='application/json')
        except Exception as e:
            data = {
                "result": str(e)
            }
            return Response(json.dumps(data, default=lambda object: object.__dict__, sort_keys=True, indent=4),
                            status=400,
                            mimetype='application/json')
