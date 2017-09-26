from basebot import abstract_api
import bittrex_api


class trade_api(abstract_api):
    def __init__(self, proxy_sett):
        self.proxy_settings = proxy_sett
        self.bittrex = bittrex_api.Bittrex(proxy_sett)

    def get_openorders(self):
        d = []
        fnd = self.bittrex.get_open_orders()
        if fnd['success']:
            fnd = fnd['result']
            for f in fnd:
                if f['Quantity'] == f['QuantityRemaining']:
                    d.append(f['OrderUuid'])
        return d

    def get_partiallyorders(self):
        d = []
        fnd = self.bittrex.get_open_orders()
        if fnd['success']:
            fnd = fnd['result']
            for f in fnd:
                if f['Quantity'] != f['QuantityRemaining']:
                    d.append(f['Exchange'])
        return d

    def get_btc_balance(self, balance):
        if 'BTC' in balance:
            return balance['BTC']
        else:
            return 0

    def get_balanses(self):
        d = {}
        fnd = self.bittrex.get_balances()
        if fnd['success']:
            fnd = fnd['result']
            for f in fnd:
                if f['Available'] > 0:
                    d[f['Currency']] = f['Available']
        return d

    def get_btc_ex(self, cur):
        return 'BTC-' + cur

    def cancel_orders(self, order_ids):
        for ods in order_ids:
            self.bittrex.cancel(ods)

    def get_min_order_size(self, mult):
        return 0.0005 * mult

    def get_down_list(self):
        d = []
        fnd = self.bittrex.get_currencies()
        if fnd['success']:
            fnd = fnd['result']
            for f in fnd:
                if not f['IsActive']:
                    d.append(f['Currency'])
        return d

    def get_coin_list(self):
        d = []
        fnd = self.bittrex.get_market_summaries()
        if fnd['success']:
            d = fnd['result']
        return d

    def get_volume(self, vol):
        return vol['Volume']

    def is_btc(self, pair):
        return ('BTC-' in pair)

    def get_pair(self, pair):
        return pair['MarketName']

    def get_low(self, pair):
        return pair['Low']

    def get_high(self, pair):
        return pair['High']

    def get_best_bid(self, pair):
        return pair['Bid']

    def get_best_ask(self, pair):
        return pair['Ask']

    def get_coin_details(self, pair):
        return self.bittrex.get_marketsummary(pair)

    def is_Error(self, req):
        return not req['success']

    def get_currency_info(self, req):
        return req['result'][0]

    def get_minask(self, pair):
        return pair['Ask']

    def get_maxbid(self, pair):
        return pair['Bid']

    def buy_currency(self, pair, quantity, price):
        self.bittrex.buy_limit(pair, quantity, price)

    def sell_currency(self, pair, quantity, price):
        self.bittrex.sell_limit(pair, quantity, price)

    def get_buy_price(self, pair):
        price = 0
        fnd = self.bittrex.get_order_history(pair)
        if fnd['success']:
            fnd = fnd['result']
            for f in fnd:
                if f['OrderType'] == 'LIMIT_BUY':
                    price = f['PricePerUnit']
                else:
                    break
        return price
