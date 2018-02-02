import requests
import json


class Request:
    def get(self, url: str, params: dict):
        response = requests.get(url, params=params)

        return self._get_result(response)

    def post(self, url: str, params: dict, data: dict, headers: dict):
        response = requests.post(url, params=params, data=data, headers=headers)

        return self._get_result(response)

    def _get_content(self, response):
        return json.loads(response.content.decode('utf-8')) if response.status_code is 200 else {
            "error": response.content,
            "status_code": response.status_code,
        }

    def _get_result(self, response):
        return {
            "status_code": response.status_code,
            "result": self._get_content(response),
            "response": response
        }
