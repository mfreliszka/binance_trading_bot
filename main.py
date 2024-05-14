import tkinter as tk
import logging

from connectors.binance_futures import BinanceFuturesClient
from os import environ

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    binance = BinanceFuturesClient(
        public_key=environ.get("API_KEY"),
        secret_key=environ.get("API_SECRET"),
        testnet=True,
    )
    root = tk.Tk()
    root.configure(bg="gray12")
 
    i = 0
    j = 0

    for contract in binance.get_contracts():
        label_widget = tk.Label(root, text=contract, bg="gray12", fg="SteelBlue1", width=13)
        label_widget.grid(row=i, column=j, sticky="ew")

        if i == 4:
            j += 1
            i = 0
        else:
            i += 1

    #print(binance.get_historical_candles("BTCUSDT", "1h"))
    #print(binance.get_bid_ask("BTCUSDT"))
    print(binance.get_balance())
    root.mainloop()

