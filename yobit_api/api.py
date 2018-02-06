from .utils import Request
from urllib.parse import urlencode
import hmac
import hashlib
import datetime


class YobitApi:
    API_URL = None

    def _make_request(self, method_name: str = None, method: str = 'get', params: dict = None, data: dict = None,
                      headers: dict = None, url_number: int = 0):
        params = {} if not params else params
        headers = {} if not headers else headers
        data = {} if not data else data

        request_url = self.API_URL[url_number].format(method_name) if method_name else self.API_URL

        if method == 'get':
            res = Request().get(request_url, params)
        elif method == 'post':
            res = Request().post(request_url, params, data, headers)
        else:
            return None

        # if answer status_code is like 50x lets try another url. This is the fastest way to come through Cloudflare
        if str(res['status_code'])[:2] == '50' and len(self.API_URL) > url_number + 1:
            return self._make_request(method_name, method, params, data, headers, url_number=url_number + 1)
        else:
            return res


class PublicApi(YobitApi):
    API_URL = [
        "https://yobit.io/api/3/{0}",
        "https://yobit.net/api/3/{0}",
    ]

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

        result = self._make_request("ticker/%s" % pair).get("result")

        return result.get(pair) if result.get(pair) else result

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

        result = self._make_request("depth/%s" % pair, params={"limit": int(limit)}).get("result")

        return result.get(pair) if result.get(pair) else result

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

        result = self._make_request("trades/%s" % pair, params={"limit": int(limit)}).get("result")

        return result.get(pair) if result.get(pair) else result

    def get_pairs_trades(self, pairs: list, limit: int = 150):
        """
        Method returns information about the last transactions for selected pairs.
        :param pairs:
        :param limit:  (on default 150 to 2000 maximum)
        :return:
        """
        str_pairs = '-'.join(pairs)

        return self._make_request("trades/%s" % str_pairs, params={"limit": int(limit)}).get("result")


class TradeApi(YobitApi):
    API_URL = [
        "https://yobit.io/tapi/",
        "https://yobit.net/tapi/"
    ]

    def __init__(self, key: str, secret_key: str):
        self.key = key
        self.secret_key = secret_key

        self.headers = {
            "Key": self.key,
            "Sign": self.key,
        }

    def _get_headers(self, data: dict):
        data['nonce'] = str(int(datetime.datetime.now().timestamp()))

        sign = hmac.new(
            self.secret_key.encode(),
            urlencode(data).encode(),
            hashlib.sha512).hexdigest()

        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sign': sign,
            'Key': self.key,
        }

    def get_info(self):
        """
        Method returns information about user's balances and priviledges of API-key as well as server time.
        :return:
        """

        data = {
            "method": "getInfo",
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def buy(self, pair: str, price: float or str, amount: float):
        """
        Method that allows creating new orders for stock exchange trading
        Requirements: priviledges of key info&trade
        :param pair:        pair (example: ltc_btc)
        :param price:       exchange rate for buying (value: float or string)
        :param amount:      amount needed for buying (value: int)
        :return:
        """

        data = {
            "method": "Trade",
            "pair": pair,
            "type": 'buy',
            "rate": price if isinstance(price, str) else '%.8f' % price,
            "amount": amount,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def sell(self, pair: str, price: float or str, amount: float):
        """
        Method that allows creating new orders for stock exchange trading
        Requirements: priviledges of key info&trade
        :param pair:        pair (example: ltc_btc)
        :param price:       exchange rate for selling (value: float or string)
        :param amount:      amount needed for selling (value: int)
        :return:
        """

        data = {
            "method": "Trade",
            "pair": pair,
            "type": "sell",
            "rate": price if isinstance(price, str) else '%.8f' % price,
            "amount": amount,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def get_active_orders(self, pair: str):
        """
        Method returns list of user's active orders
        :param pair:        pair (example: ltc_btc)
        :return:
        """

        data = {
            "method": "ActiveOrders",
            "pair": pair,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def get_order(self, order_id: int):
        """
        Method returns detailed information about the chosen order
        :param order_id:        order ID
        :return:
        """

        data = {
            "method": "OrderInfo",
            "order_id": int(order_id),
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def cancel_order(self, order_id: int):
        """
        Method cancels the chosen order
        :param order_id:        order ID
        :return:
        """

        data = {
            "method": "CancelOrder",
            "order_id": int(order_id),
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def get_trade_history(self, pair: str, start: int = 0, count: int = 1000, from_id: int = 0, end_id: int = None,
                          order: str = "DESC", start_time: int = 0, end_time: int = None):
        """
        Method returns transaction history.
        :param pair:            pair (example: ltc_btc)
        :param start:           No. of transaction from which withdrawal starts (value: numeral, on default: 0)
        :param count:           quantity of withrawal transactions (value: numeral, on default: 1000)
        :param from_id:         ID of transaction from which withdrawal starts (value: numeral, on default: 0)
        :param end_id:          ID of transaction at which withdrawal finishes (value: numeral, on default: ∞)
        :param order:           sorting at withdrawal (value: ASC or DESC, on default: DESC)
        :param start_time:      the time to start the display (value: unix time, on default: 0)
        :param end_time:        the time to end the display (value: unix time, on default: ∞)
        :return:
        """
        if order not in ['DESC', 'ASC']:
            raise Exception('order should be `DESC` or `ASC')

        data = {
            "method": "TradeHistory",
            "pair": pair,
            "from": start,
            "count": count,
            "from_id": from_id,
            "end_id": end_id,
            "order": order,
            "since": start_time,
            "end": end_time,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def get_address(self, coin_name: str, need_new: bool = False):
        """
        Method returns deposit address.
        :param coin_name:        ticker (example: BTC)
        :param need_new:
        :return:
        """

        data = {
            "method": "GetDepositAddress",
            "coinName": coin_name,
            "need_new": int(need_new),
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def withdraw_coins(self, coin_name: str, amount: float, address: str):
        """
        Method creates withdrawal request.
        Requirements: priviledges of key withdrawals
        :param coin_name:        ticker (example: BTC)
        :param amount:           amount to withdraw
        :param address:         destination address
        :return:
        """

        data = {
            "method": "WithdrawCoinsToAddress",
            "coinName": coin_name,
            "amount": amount,
            "address": address,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def create_coupon(self, coin_name: str, amount: float):
        """
        Method allows you to create Yobicodes (coupons).
        Requirements: priviledges of key withdrawals
        :param coin_name:        ticker (example: BTC)
        :param amount:           amount of yobicode
        :return:
        """

        data = {
            "method": "CreateCoupon",
            "currency": coin_name,
            "amount": amount,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")

    def redeem_coupon(self, coupon: str):
        """
        Method is used to redeem Yobicodes (coupons).
        :param coupon:           yobicode to redeem (example: YOBITUZ0HHSTB...OQX3H01BTC)
        :return:
        """

        data = {
            "method": "RedeemCoupon",
            "coupon": coupon,
        }

        return self._make_request(method="post", data=data, headers=self._get_headers(data)).get("result")
