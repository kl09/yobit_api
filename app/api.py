from .utils import Request


class PublicApi:
    API_URL = "https://yobit.net/api/3/{0}"

    def _make_request(self, method_name: str, method='get', params=None):
        params = {} if not params else params
        request_url = self.API_URL.format(method_name)

        if method == 'get':
            return Request().get(request_url, params)

    def get_info(self):
        """
        list of active pairs.
        :return:
        """
        return self._make_request("info").get("result")

    def get_pair_ticker(self, pair: str):
        """
        Method provides statistic data for the last 24 hours.
        :param pair:
        :return:
        """

        return self._make_request("ticker/%s" % pair).get("result")

    def get_pairs_ticker(self, pairs: list):
        """
        Method provides statistic for the selected pairs for the last 24 hours.
        :param pairs:
        :return:
        """
        str_pairs = '-'.join(pairs)

        return self._make_request("ticker/%s" % str_pairs).get("result")

    def get_pair_depth(self, pair: str, limit: int = 150):
        """
        Method returns information about lists of active orders for pair
        :param pair:
        :param limit:  (on default 150 to 2000 maximum)
        :return:
        """

        return self._make_request("depth/%s" % pair, params={"limit": int(limit)}).get("result")

    def get_pairs_depth(self, pairs: list, limit: int = 150):
        """
        Method returns information about lists of active orders for selected pairs.
        :param pairs:
        :param limit:  (on default 150 to 2000 maximum)
        :return:
        """
        str_pairs = '-'.join(pairs)

        return self._make_request("depth/%s" % str_pairs, params={"limit": int(limit)}).get("result")

    def get_pair_trades(self, pair: str, limit: int = 150):
        """
        Method returns information about the last transactions for pair.
        :param pair:
        :param limit:  (on default 150 to 2000 maximum)
        :return:
        """

        return self._make_request("trades/%s" % pair, params={"limit": int(limit)}).get("result")

    def get_pairs_trades(self, pairs: list, limit: int = 150):
        """
        Method returns information about the last transactions for selected pairs.
        :param pairs:
        :param limit:  (on default 150 to 2000 maximum)
        :return:
        """
        str_pairs = '-'.join(pairs)

        return self._make_request("trades/%s" % str_pairs, params={"limit": int(limit)}).get("result")
