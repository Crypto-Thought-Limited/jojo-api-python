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

    def authenticate(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        message = json.dumps(payload, sort_keys=True)
        signature = self.sign_message(message)
        headers = {
            'JOJO-PUBLIC-KEY': self.public_key,
            'JOJO-SIGNATURE': signature,
            'JOJO-PAYLOAD': message
        }
        return requests.get(self.base_url + endpoint, headers=headers)

    def get_data(self, endpoint):
        response = self.authenticate(endpoint)
        return response.json()

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
