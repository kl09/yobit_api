
Yobit API Python wrapper.
=========================

## Install
```bash
pip3 install git+https://git@github.com/kl09/yobit_api.git
```

>

Example for PublicApi:

```python
import yobit_api
res = yobit_api.PublicApi().get_pair_ticker(pair="btc_usd")
```


>

Example for TradeApi:

```python
import yobit_api
res = yobit_api.TradeApi(key="yobit_key", secret_key="yobit_secret_key").get_info()
```

By default you can use Cloudflare scrape. This module helps to bypass Cloudflare's anti-bot page.

Star it if u like

