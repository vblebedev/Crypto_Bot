import time
import hmac
import hashlib
from urllib.parse import urlencode
import requests
from bittrex_api import client_secret
from bittrex_api import client_key

BUY_ORDERBOOK = 'buy'
SELL_ORDERBOOK = 'sell'
BOTH_ORDERBOOK = 'both'

BASE_URL = 'https://bittrex.com/api/v1.1/%s/'

MARKET_SET = {
    'getopenorders',
    'cancel',
    'sellmarket',
    'selllimit',
    'buymarket',
    'buylimit'
}

ACCOUNT_SET = {
    'getbalances',
    'getbalance',
    'getdepositaddress',
    'withdraw',
    'getorderhistory',
    'getorder',
    'getdeposithistory',
    'getwithdrawalhistory'
}


class Bittrex(object):
    def __init__(self, proxy_sett):
        self.proxy_settings = proxy_sett

    def using_requests(self, request_url, apisign):
        if self.proxy_settings['proxy_used']:
            return requests.get(
                request_url,
                headers={"apisign": apisign},
                proxies=self.proxy_settings['proxyDict']
            ).json()
        else:
            return requests.get(
                request_url,
                headers={"apisign": apisign}
            ).json()

    def api_query(self, method, options=None):
        """
        Queries Bittrex with given method and options
        :param method: Query method for getting info
        :type method: str
        :param options: Extra options for query
        :type options: dict
        :return: JSON response from Bittrex
        :rtype : dict
        """
        if not options:
            options = {}
        nonce = str(int(time.time() * 1000))
        method_set = 'public'

        if method in MARKET_SET:
            method_set = 'market'
        elif method in ACCOUNT_SET:
            method_set = 'account'

        request_url = (BASE_URL % method_set) + method + '?'

        if method_set != 'public':
            request_url += 'apikey=' + client_key + "&nonce=" + nonce + '&'

        request_url += urlencode(options)

        apisign = hmac.new(client_secret.encode(),
                           request_url.encode(),
                           hashlib.sha512).hexdigest()
        return self.using_requests(request_url, apisign)

    def get_markets(self):
        """
        Used to get the open and available trading markets
        at Bittrex along with other meta data.
        :return: Available market info in JSON
        :rtype : dict
        """
        return self.api_query('getmarkets')

    def get_currencies(self):
        """
        Used to get all supported currencies at Bittrex
        along with other meta data.
        :return: Supported currencies info in JSON
        :rtype : dict
        """
        return self.api_query('getcurrencies')

    def get_ticker(self, market):
        """
        Used to get the current tick values for a market.
        :param market: String literal for the market (ex: BTC-LTC)
        :type market: str
        :return: Current values for given market in JSON
        :rtype : dict
        """
        return self.api_query('getticker', {'market': market})

    def get_market_summaries(self):
        """
        Used to get the last 24 hour summary of all active exchanges
        :return: Summaries of active exchanges in JSON
        :rtype : dict
        """
        return self.api_query('getmarketsummaries')

    def get_marketsummary(self, market):
        """
        Used to get the last 24 hour summary of all active exchanges in specific coin
        :param market: String literal for the market(ex: BTC-XRP)
        :type market: str
        :return: Summaries of active exchanges of a coin in JSON
        :rtype : dict
        """
        return self.api_query('getmarketsummary', {'market': market})

    def get_orderbook(self, market, depth_type, depth=20):
        """
        Used to get retrieve the orderbook for a given market
        :param market: String literal for the market (ex: BTC-LTC)
        :type market: str
        :param depth_type: buy, sell or both to identify the type of orderbook to return.
            Use constants BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
        :type depth_type: str
        :param depth: how deep of an order book to retrieve. Max is 100, default is 20
        :type depth: int
        :return: Orderbook of market in JSON
        :rtype : dict
        """
        return self.api_query('getorderbook', {'market': market, 'type': depth_type, 'depth': depth})

    def get_market_history(self, market, count):
        """
        Used to retrieve the latest trades that have occurred for a
        specific market.
        /market/getmarkethistory
        :param market: String literal for the market (ex: BTC-LTC)
        :type market: str
        :param count: Number between 1-100 for the number of entries to return (default = 20)
        :type count: int
        :return: Market history in JSON
        :rtype : dict
        """
        return self.api_query('getmarkethistory', {'market': market, 'count': count})

    def buy_limit(self, market, quantity, rate):
        """
        Used to place a buy order in a specific market. Use buylimit to place
        limit orders Make sure you have the proper permissions set on your
        API keys for this call to work
        /market/buylimit
        :param market: String literal for the market (ex: BTC-LTC)
        :type market: str
        :param quantity: The amount to purchase
        :type quantity: float
        :param rate: The rate at which to place the order.
            This is not needed for market orders
        :type rate: float
        :return:
        :rtype : dict
        """
        return self.api_query('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def sell_limit(self, market, quantity, rate):
        """
        Used to place a sell order in a specific market. Use selllimit to place
        limit orders Make sure you have the proper permissions set on your
        API keys for this call to work
        /market/selllimit
        :param market: String literal for the market (ex: BTC-LTC)
        :type market: str
        :param quantity: The amount to purchase
        :type quantity: float
        :param rate: The rate at which to place the order.
            This is not needed for market orders
        :type rate: float
        :return:
        :rtype : dict
        """
        return self.api_query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def cancel(self, uuid):
        """
        Used to cancel a buy or sell order
        /market/cancel
        :param uuid: uuid of buy or sell order
        :type uuid: str
        :return:
        :rtype : dict
        """
        return self.api_query('cancel', {'uuid': uuid})

    def get_open_orders(self, market=None):
        """
        Get all orders that you currently have opened. A specific market can be requested
        /market/getopenorders
        :param market: String literal for the market (ie. BTC-LTC)
        :type market: str
        :return: Open orders info in JSON
        :rtype : dict
        """
        if market is None:
            return self.api_query('getopenorders')
        else:
            return self.api_query('getopenorders', {'market': market})

    def get_balances(self):
        """
        Used to retrieve all balances from your account
        /account/getbalances
        :return: Balances info in JSON
        :rtype : dict
        """
        return self.api_query('getbalances', {})

    def get_balance(self, currency):
        """
        Used to retrieve the balance from your account for a specific currency
        /account/getbalance
        :param currency: String literal for the currency (ex: LTC)
        :type currency: str
        :return: Balance info in JSON
        :rtype : dict
        """
        return self.api_query('getbalance', {'currency': currency})

    def get_deposit_address(self, currency):
        """
        Used to generate or retrieve an address for a specific currency
        /account/getdepositaddress
        :param currency: String literal for the currency (ie. BTC)
        :type currency: str
        :return: Address info in JSON
        :rtype : dict
        """
        return self.api_query('getdepositaddress', {'currency': currency})

    def withdraw(self, currency, quantity, address):
        """
        Used to withdraw funds from your account
        /account/withdraw
        :param currency: String literal for the currency (ie. BTC)
        :type currency: str
        :param quantity: The quantity of coins to withdraw
        :type quantity: float
        :param address: The address where to send the funds.
        :type address: str
        :return:
        :rtype : dict
        """
        return self.api_query('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})

    def get_order_history(self, market=None):
        """
        Used to reterieve order trade history of account
        /account/getorderhistory
        :param market: optional a string literal for the market (ie. BTC-LTC). If ommited, will return for all markets
        :type market: str
        :param count: optional  the number of records to return
        :type count: int
        :return: order history in JSON
        :rtype : dict
        """
        if not market:
            return self.api_query('getorderhistory')
        else:
            return self.api_query('getorderhistory', {'market': market})

    def get_order(self, uuid):
        """
        Used to get details of buy or sell order
        /account/getorder
        :param uuid: uuid of buy or sell order
        :type uuid: str
        :return:
        :rtype : dict
        """
        return self.api_query('getorder', {'uuid': uuid})

    def get_withdrawal_history(self, currency=None):
        if currency is None:
            params = {}
        else:
            params = {'currency': currency}

        return self.api_query('getwithdrawalhistory', params)

    def get_deposit_history(self, currency=None):
        if currency is None:
            params = {}
        else:
            params = {'currency': currency}

        return self.api_query('getdeposithistory', params)
