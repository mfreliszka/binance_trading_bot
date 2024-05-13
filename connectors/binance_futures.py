import logging
import requests
import base_urls
logger = logging.getLogger()




class BinanceFuturesClient:
    def __init__(self, testnet: bool):
        self.prices = dict()

        if testnet:
            self.base_url = base_urls.TESTNET_BASE_URL
        else:
            self.base_url = base_urls.BASE_URL
    
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