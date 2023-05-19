"""
coding:UTF-8
Author: Hunter & ChatGPT
Date: 2023-5-18
"""

import json
import requests
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
        if payload is None:
            payload = {}
        message = json.dumps(payload, sort_keys=True)
        signature = self.sign_message(message)
        headers = {
            'JOJO-PUBLIC-KEY': self.public_key,
            'JOJO-SIGNATURE': signature,
            'JOJO-PAYLOAD': message
        }
        url = self.base_url + endpoint
        if method.lower() == 'get':
            return requests.get(url, headers=headers)
        elif method.lower() == 'post':
            return requests.post(url, headers=headers, json=payload)
        elif method.lower() == 'delete':
            return requests.delete(url, headers=headers, json=payload)

    def post_data(self, endpoint, payload=None):
        return self.authenticate('post', endpoint, payload).json()

    def get_data(self, endpoint, payload=None):
        return self.authenticate('get', endpoint, payload).json()

    def delete_data(self, endpoint, payload=None):
        return self.authenticate('delete', endpoint, payload).json()

    def get_time(self):
        endpoint = "/v1/time"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_exchange_info(self):
        endpoint = "/v1/exchangeInfo"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_orderbook(self):
        endpoint = "/v1/orderbook"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_trades(self):
        endpoint = "/v1/trades"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_historical_trades(self):
        endpoint = "/v1/historicalTrades"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_klines(self):
        endpoint = "/v1/klines"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_funding_rate(self):
        endpoint = "/v1/fundingRate"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_risky_accounts(self):
        endpoint = "/v1/riskyAccounts"
        response = requests.get(self.base_url + endpoint)
        return response.json()

    # Account endpoints
    def post_account(self, payload):
        return self.post_data("/v1/account", payload)

    def get_account(self):
        return self.get_data("/v1/account")

    # Order endpoints
    def post_order_build(self, payload):
        return self.post_data("/v1/order/build", payload)

    def post_order(self, payload):
        return self.post_data("/v1/order", payload)

    def delete_order(self, payload):
        return self.delete_data("/v1/order", payload)

    def delete_all_open_orders(self, payload):
        return self.delete_data("/v1/allOpenOrders", payload)

    def get_history_orders(self):
        return self.get_data("/v1/historyOrders")

    def get_order(self):
        return self.get_data("/v1/order")

    def get_open_order(self):
        return self.get_data("/v1/openOrder")

    def get_open_orders(self):
        return self.get_data("/v1/openOrders")

    def get_user_trades(self):
        return self.get_data("/v1/userTrades")

    def get_incomes(self):
        return self.get_data("/v1/incomes")

    def get_balances(self):
        return self.get_data("/v1/balances")

    def get_positions(self):
        return self.get_data("/v1/positions")

# usage


api_client = JojoAPI('https://api.jojo.exchange', '<your-private-key-here>')
print(api_client.get_time())
print(api_client.get_exchange_info())
print(api_client.get_orderbook())
print(api_client.get_trades())
print(api_client.get_historical_trades())
print(api_client.get_klines())
print(api_client.get_funding_rate())
print(api_client.get_risky_accounts())
payload = {}  # TODO: Replace with actual payload
print(api_client.post_account(payload))
print(api_client.get_account())
print(api_client.post_order_build(payload))
print(api_client.post_order(payload))
print(api_client.delete_order(payload))
print(api_client.delete_all_open_orders(payload))
print(api_client.get_history_orders())
print(api_client.get_order())
print(api_client.get_open_order())
print(api_client.get_open_orders())
print(api_client.get_user_trades())
print(api_client.get_incomes())
print(api_client.get_balances())
print(api_client.get_positions())