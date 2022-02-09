import json

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiTestView(APIView):
    """接口测试视图"""

    def post(self, request):
        data = request.data
        params = {item.get("key"): item.get("value") for item in data.get("params")}
        headers = {item.get("key"): item.get("value") for item in data.get("headers")}
        cookies = {item.get("key"): item.get("value") for item in data.get("cookies")}

        if 'json' in json.dumps(headers):
            data["body"] = json.dumps(data.get("body"))

        response = requests.request(method=data.get("method"), url=data.get("url"), data=data.get("body"),
                                    params=params, headers=headers, cookies=cookies)

        res = Response(status=status.HTTP_200_OK,
                       data={"code": response.status_code, "headers": response.headers})

        if 'json' in json.dumps(dict(response.headers)):
            res.data['body'] = response.json()
        else:
            res.data['body'] = response.text

        return res
