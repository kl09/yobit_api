import requests
import json
import cfscrape

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance


class Request:
    def get(self, url: str, params: dict, use_cloudflare_scrape: bool):
        obj = requests if not use_cloudflare_scrape else scraper
        response = obj.get(url, params=params)

        return self._get_result(response)

    def post(self, url: str, params: dict, data: dict, headers: dict, use_cloudflare_scrape: bool):
        obj = requests if not use_cloudflare_scrape else scraper
        response = obj.post(url, params=params, data=data, headers=headers)

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
