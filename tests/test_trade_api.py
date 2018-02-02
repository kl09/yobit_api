import unittest
from app.api import TradeApi

YOBIT_KEY = ''
YOBIT_SECRET_KEY = ''


class TradeTests(unittest.TestCase):
    def setUp(self):
        if not YOBIT_KEY and not YOBIT_SECRET_KEY:
            raise Exception('you should provide keys fof trade tests')

    def test_info(self):
        res = TradeApi(YOBIT_KEY, YOBIT_SECRET_KEY).get_info()

        self.assertEqual(1, res['success'])
        self.assertIsNotNone(res['return'])

    def test_get_active_orders(self):
        res = TradeApi(YOBIT_KEY, YOBIT_SECRET_KEY).get_active_orders(pair='btc_usd')

        self.assertEqual(1, res['success'])


if __name__ == '__main__':
    unittest.main()
