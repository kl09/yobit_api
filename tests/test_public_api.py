import unittest
from app.api import PublicApi
from time import sleep


class InfoTests(unittest.TestCase):
    def test_info(self):
        res = PublicApi().get_info()

        b = True if len(res['pairs']) > 500 else False
        self.assertEqual(True, b)


class TickerTests(unittest.TestCase):
    def setUp(self):
        # or u will get `rate limited and banned`
        sleep(0.3)

    def test_valid_ticker(self):
        res = PublicApi().get_pair_ticker(pair="ltc_btc")

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

    def test_invalid_ticker(self):
        res = PublicApi().get_pair_ticker(pair="ltc_btcAa")
        self.assertEqual(404, res.get("status_code"))

        res = PublicApi().get_pair_ticker(pair="ltc_btc23")
        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: ltc_btc23", res.get("error"))

    def test_valid_tickers(self):
        res = PublicApi().get_pairs_ticker(pairs=['ltc_btc', 'btc_usd', 'etc_btc'])

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("btc_usd"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("etc_btc"))

    def test_invalid_tickers(self):
        res = PublicApi().get_pairs_ticker(pairs=['ltc_btc', 'test', 'etc_btc'])

        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: test", res.get("error"))


class DepthTests(unittest.TestCase):
    def setUp(self):
        # or u will get `rate limited and banned`
        sleep(0.3)

    def test_valid_depth(self):
        res = PublicApi().get_pair_depth(pair="ltc_btc")

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

    def test_invalid_depth(self):
        res = PublicApi().get_pair_depth(pair="ltc_btcAa")
        self.assertEqual(404, res.get("status_code"))

        res = PublicApi().get_pair_depth(pair="ltc_btc23")
        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: ltc_btc23", res.get("error"))

    def test_valid_depths(self):
        res = PublicApi().get_pairs_depth(pairs=['ltc_btc', 'btc_usd', 'etc_btc'])

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("btc_usd"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("etc_btc"))

    def test_invalid_depths(self):
        res = PublicApi().get_pairs_depth(pairs=['ltc_btc', 'test', 'etc_btc'])

        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: test", res.get("error"))

    def test_depth_limit(self):
        res = PublicApi().get_pair_depth(pair="ltc_btc", limit=166)
        self.assertEqual(166, len(res['ltc_btc']['bids']))

        res = PublicApi().get_pair_depth(pair="ltc_btc", limit=177)
        self.assertEqual(177, len(res['ltc_btc']['bids']))

    def test_depths_limit(self):
        res = PublicApi().get_pairs_depth(pairs=['ltc_btc', 'btc_usd', 'etc_btc'], limit=177)

        self.assertEqual(177, len(res['ltc_btc']['bids']))
        self.assertEqual(177, len(res['btc_usd']['bids']))
        self.assertEqual(177, len(res['etc_btc']['bids']))


class TradeTests(unittest.TestCase):
    def setUp(self):
        # or u will get `rate limited and banned`
        sleep(0.3)

    def test_valid_trade(self):
        res = PublicApi().get_pair_trades(pair="ltc_btc")

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

    def test_invalid_trade(self):
        res = PublicApi().get_pair_trades(pair="ltc_btcAa")
        self.assertEqual(404, res.get("status_code"))

        res = PublicApi().get_pair_trades(pair="ltc_btc23")
        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: ltc_btc23", res.get("error"))

    def test_valid_trades(self):
        res = PublicApi().get_pairs_trades(pairs=['ltc_btc', 'btc_usd', 'etc_btc'])

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("ltc_btc"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("btc_usd"))

        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("etc_btc"))

    def test_invalid_trades(self):
        res = PublicApi().get_pairs_trades(pairs=['ltc_btc', 'test', 'etc_btc'])

        self.assertEqual(0, res.get("success"))
        self.assertEqual("Invalid pair name: test", res.get("error"))

    def test_trade_limit(self):
        res = PublicApi().get_pair_trades(pair="ltc_btc", limit=166)

        self.assertEqual(166, len(res['ltc_btc']))

        res = PublicApi().get_pair_trades(pair="ltc_btc", limit=177)
        self.assertEqual(177, len(res['ltc_btc']))

    def test_trades_limit(self):
        res = PublicApi().get_pairs_trades(pairs=['ltc_btc', 'btc_usd', 'etc_btc'], limit=177)

        self.assertEqual(177, len(res['ltc_btc']))
        self.assertEqual(177, len(res['btc_usd']))
        self.assertEqual(177, len(res['etc_btc']))


if __name__ == '__main__':
    unittest.main()
