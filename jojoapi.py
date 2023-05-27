"""
coding:UTF-8
Author: Hunter & ChatGPT
Date: 2023-5-18
"""
import datetime
import json
import requests
import urllib
from web3.auto import w3


class JojoAPI:
    def __init__(self, base_url, private_key):
        self.base_url = base_url
        self.private_key = private_key
        self.public_key = self.get_public_key_from_private()

    def get_public_key_from_private(self):
        return w3.eth.account.from_key(self.private_key).address

    def sign_message(self, message):
        message_hash = w3.keccak(text=message)
        signed_message = w3.eth.account.signHash(message_hash, private_key=self.private_key)
        return signed_message.signature

    def authenticate(self, method, endpoint, payload=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if payload is None:
            payload = {}
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        payload['timestamp'] = timestamp
        sorted_params_str = json.dumps(payload, sort_keys=True)
        sorted_params = json.loads(sorted_params_str)
        url_params = urllib.parse.urlencode(sorted_params)
        message = '\x19Ethereum Signed Message:\n{}{}'.format(len(url_params), url_params)
        signature = self.sign_message(message)
        url = self.base_url + endpoint
        post_data = url_params + '&signature={}'.format(signature.hex())
        if method.lower() == 'get':
            return requests.get(url, post_data, headers=headers)
        elif method.lower() == 'post':
            return requests.post(url, post_data, headers=headers)
        elif method.lower() == 'delete':
            return requests.delete(url + '?' + post_data, headers=headers)

    def post_data(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        if payload.get('account') is None:
            payload['account'] = self.public_key
        return self.authenticate('post', endpoint, payload).json()

    def get_data(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        if payload.get('account') is None:
            payload['account'] = self.public_key
        return self.authenticate('get', endpoint, payload).json()

    def delete_data(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        if payload.get('account') is None:
            payload['account'] = self.public_key
        return self.authenticate('delete', endpoint, payload)

    def get_time(self):
        endpoint = "/v1/time"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_exchange_info(self):
        endpoint = "/v1/exchangeInfo"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_orderbook(self, **kwargs):
        endpoint = "/v1/orderbook"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_trades(self, **kwargs):
        endpoint = "/v1/trades"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_historical_trades(self, **kwargs):
        endpoint = "/v1/historicalTrades"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_klines(self, **kwargs):
        endpoint = "/v1/klines"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_mark_price_klines(self, **kwargs):
        endpoint = "/v1/klines"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_funding_rate(self, **kwargs):
        endpoint = "/v1/fundingRate"
        params = urllib.parse.urlencode(kwargs)
        response = requests.get(self.base_url + endpoint, params)
        return response.json()

    def get_risky_accounts(self):
        endpoint = "/v1/riskyAccounts"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    # Account endpoints
    def post_account(self, **kwargs):
        return self.post_data('/v1/account', kwargs)

    def get_account(self, **kwargs):
        return self.get_data("/v1/account", kwargs)

    # Order endpoints
    def post_order_build(self, **kwargs):
        return self.post_data("/v1/order/build", kwargs)

    def post_order(self, **kwargs):
        order_build = self.post_data("/v1/order/build", kwargs)
        if order_build.get('orderHash') is None:
            return order_build
        order_hash = order_build['orderHash']
        kwargs['info'] = order_build['order']['info']
        signed_message = w3.eth.account.signHash(order_hash, private_key=self.private_key)
        kwargs['orderSignature'] = signed_message.signature.hex()
        return self.post_data("/v1/order", kwargs)

    def delete_order(self, **kwargs):
        return self.delete_data("/v1/order", kwargs)

    def delete_all_open_orders(self, **kwargs):
        return self.delete_data("/v1/allOpenOrders", kwargs)

    def get_history_orders(self, **kwargs):
        return self.get_data("/v1/historyOrders", kwargs)

    def get_order(self, **kwargs):
        return self.get_data("/v1/order", kwargs)

    def get_open_order(self, **kwargs):
        return self.get_data("/v1/openOrder", kwargs)

    def get_open_orders(self, **kwargs):
        return self.get_data("/v1/openOrders", kwargs)

    def get_user_trades(self, **kwargs):
        return self.get_data("/v1/userTrades", kwargs)

    def get_incomes(self, **kwargs):
        return self.get_data("/v1/incomes", kwargs)

    def get_balances(self, **kwargs):
        return self.get_data("/v1/balances", kwargs)

    def get_positions(self, **kwargs):
        return self.get_data("/v1/positions", kwargs)

# usage


api_client = JojoAPI('https://api.arbitrum.jojo.exchange', '<your-private-key-here>')

# public endpoint
print(api_client.get_time())
print(api_client.get_exchange_info())
print(api_client.get_orderbook(marketId='btcusdc'))
print(api_client.get_trades(marketId='ethusdc'))
print(api_client.get_historical_trades(marketId='btcusdc'))
print(api_client.get_klines(marketId='ethusdc', interval='1D'))
print(api_client.get_mark_price_klines(marketId='btcusdc', interval='1D'))
print(api_client.get_funding_rate(marketId='btcusdc', limit=500))
print(api_client.get_risky_accounts())

# private endpoint
print(api_client.post_account())
print(api_client.get_account())
print(api_client.post_order_build(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC'))
print(api_client.post_order(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC'))
print(api_client.delete_order(marketId='ethusdc', orderId='51597754450176'))
print(api_client.delete_all_open_orders(marketId='ethusdc'))
print(api_client.get_history_orders(marketId='ethusdc'))
print(api_client.get_order(marketId='ethusdc', orderId='51597754450176'))
print(api_client.get_open_order(marketId='ethusdc', orderId='51597754450176'))
print(api_client.get_open_orders(marketId='ethusdc'))
print(api_client.get_user_trades(marketId='ethusdc'))
print(api_client.get_incomes(marketId='ethusdc'))
print(api_client.get_balances())
print(api_client.get_positions())

# authorized from other subaccount e.g. 0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c
# print(api_client.post_account(account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_account(account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.post_order_build(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.post_order(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.delete_order(marketId='ethusdc', orderId='51597754450176', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.delete_all_open_orders(marketId='ethusdc', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_history_orders(marketId='ethusdc', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_order(marketId='ethusdc', orderId='51597754450176', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_open_order(marketId='ethusdc', orderId='51597754450176', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_open_orders(marketId='ethusdc', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_user_trades(marketId='ethusdc', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_incomes(marketId='ethusdc', account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_balances(account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
# print(api_client.get_positions(account='0x7C3CbDD9422a21dF7cf0e1E9b20E7A80049b417c'))
