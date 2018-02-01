import requests
import json


class Request:
    def get(self, url: str, params: dict):
        response = requests.get(url, params=params)

        return {
            "status_code": response.status_code,
            "result": self._get_content(response),
            "response": response
        }

    def _get_content(self, response):
        return json.loads(response.content.decode('utf-8')) if response.status_code is 200 else {
            "error": response.content,
            "status_code": response.status_code,
        }
