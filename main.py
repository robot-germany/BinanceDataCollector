import os
from dotenv import load_dotenv
import api_handling
import data_processing
import BinanceAPIHandler

load_dotenv()
apikey = os.getenv("apiKey")
secretkey = os.getenv("secretKey")
interval = os.getenv("interval")

if __name__ == '__main__':

    all_isolated_margin_symbols = BinanceAPIHandler.symbols(api_key=apikey, api_secret=secretkey)

    interval_sites = [
        [f'https://api.binance.com/api/v3/klines?symbol={margin_symbol["symbol"]}&interval={interval}',
         margin_symbol["symbol"]] for margin_symbol in all_isolated_margin_symbols
    ]

    downloaded_sites = api_handling.download_all_sites(interval_sites)

    organized_data = {symbol: data_processing.framed_candles(data) for data, symbol in downloaded_sites}

    print(organized_data)
