import requests
from hashlib import sha256
import hmac
import time
from urllib.parse import urlencode
import logging

REST_BASE = 'https://api.binance.com/sapi'


def api_signed_request(method, path, api_key, api_secret, params=None):
    retries = 10

    while retries > 0:
        try:
            param_encode = urlencode(sorted(params.items()))
            query = f'{param_encode}&recvWindow=5000&timestamp={int(time.time() * 1000)}'
            signature = hmac.new(bytes(api_secret.encode('utf-8')),
                                 query.encode('utf-8'), sha256).hexdigest()
            urlquery = f'{REST_BASE}{path}?{query}&signature={signature}'

            logging.debug(f'REST: Attempting request: [{urlquery}]')

            api_resp = requests.request(method, urlquery,
                                        headers={'X-MBX-APIKEY': api_key})
            data = api_resp.json()
        except Exception as error:
            data = {'fatal': {'type': 'CONNECTION_ERROR', 'message': str(error)}}

        checkcode = data_check(data, urlquery)

        if checkcode[1] == '':
            if checkcode[0] in (0, 1):
                return data
        else:
            if checkcode[0] == -1:
                return False
            retries -= 1

    return False


def data_check(data, urlQuery):
    """
        This will check the data received from the exchange to
        see if there are any errors and handles them.
    """

    logMessage = 'data: {0}, query: {1}'.format(data, urlQuery)

    if 'fatal' in data:
        error = data['fatal']['message']
        errorMsg = 'error: {0}, query: {1}'.format(error, urlQuery)
        logging.warning(errorMsg)
        return 0, ''

    if data is None:
        logging.warning('Data was empty.')
        return 0, ''

    if 'code' in data:
        if str(data['code']) == '-1003':
            # code -1003 : Too many requests (>1200 per min).
            logging.warning(logMessage)
            time.sleep(30)
            return 0, ''
        if str(data['code']) == '-1013':
            # code -1013 : Invalid quantity for placing order.
            logging.warning(logMessage)
            return -1, str(data['code'])
        if str(data['code']) == '-1021':
            # code -1021 : Request outside of the recive window.
            logging.warning(logMessage)
            time.sleep(4)
            return 0, ''
        if str(data['code']) == '-2010':
            # code -2010 : Account has insufficient balance for request.
            logging.warning(f'[{logMessage}] msg: {data["msg"]}')
            return -1, str(data['code'])
        else:
            logging.warning(f'NEW ERROR: [{logMessage}] code: {data["code"]},'
                            f' msg: {data["msg"]}')
            return -1, str(data['code'])

    return 1, ''


def symbols(api_key, api_secret):
    list_of_symbols = []
    response = api_signed_request('GET', '/v1/margin/isolated/allPairs',
                                  api_key, api_secret, {})

    for d in response:
        if (d.get('quote') == 'USDT' and
                d.get('isMarginTrade') and
                d.get('isBuyAllowed') and
                d.get('isSellAllowed')):
            list_of_symbols.append({'symbol': d['symbol'], 'base': d['base']})

    return list_of_symbols
