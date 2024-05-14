import logging
import requests
import base_urls

from urllib.parse import urlencode
import hmac
from hashlib import sha256
from time import time

logger = logging.getLogger()




class BinanceFuturesClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool):
        if testnet:
            self.base_url = base_urls.TESTNET_BASE_URL
        else:
            self.base_url = base_urls.BASE_URL
    
        self.public_key: str = public_key
        self.secret_key: str = secret_key

        self.headers = {"X-MBX-APIKEY": self.public_key}
        self.prices = dict()

        logger.info("Binance Futures Client initialized successfully")

    def generate_signature(self, data):
        return hmac.new(str(self.secret_key).encode(), urlencode(data).encode(), sha256).hexdigest()
 
    def make_request(self, method, endpoint, data):
        if method == "GET":
            response = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error while making {method} request to {endpoint}: {response.json()} Status Code:{response.status_code}")
            return None

    def get_contracts(self) -> dict:
        """Get Binance Futures trading pairs."""
        exchange_info = self.make_request("GET", base_urls.EXCHANGE_INFO, None)
        contracts: dict = dict()
        
        if exchange_info is not None:
            for contract_data in exchange_info["symbols"]:
                contracts[contract_data["pair"]] = contract_data

        return contracts

    def get_historical_candles(self, symbol: str, interval):
        data: dict = dict()
        data["symbol"] = symbol
        data["interval"] = interval
        data["limit"] = 1000

        raw_candles = self.make_request("GET", base_urls.KLINES, data)
        candles = []

        if raw_candles is not None:
            for candle in raw_candles:
                candles.append(
                    [
                        candle[0], # timestamp
                        float(candle[1]), # open price
                        float(candle[2]), # high price
                        float(candle[3]), # low price
                        float(candle[4]), # close price
                        float(candle[5]), # volume
                    ]
                )

        return candles

    def get_bid_ask(self, symbol: str):
        data: dict = dict()
        data["symbol"] = symbol

        ob_data = self.make_request("GET", base_urls.BOOK_TICKER, data)
        if ob_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {
                    "bid": ob_data["bidPrice"],
                    "ask": ob_data["askPrice"],
                }
            else:
                self.prices[symbol]["bid"] = ob_data["bidPrice"]
                self.prices[symbol]["ask"] = ob_data["askPrice"]

        return self.prices

    def get_balance(self):
        data = dict()
        data["timestamp"] = int(time() * 1000) # miliseconds
        data["signature"] = self.generate_signature(data)

        balances = dict()

        account_data = self.make_request("GET", base_urls.ACCOUNT, data)

        if account_data is not None:
            for asset in account_data["assets"]:
                balances[asset["asset"]] = account_data
    
        return balances
