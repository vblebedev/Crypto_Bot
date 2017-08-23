class abstract_api():
    def get_coin_list(self):
        pass

    def get_down_list(self):
        d = []
        return d

    def get_coin_details(self, pair):
        pass

    def get_volume(self, vol):
        pass

    def is_btc(self, pair):
        return False

    def get_pair(self, pair):
        pass

    def get_low(self, pair):
        pass

    def get_high(self, pair):
        pass

    def is_Error(self, req):
        return False

    def get_currency_info(self, req):
        pass

    def get_minask(self, pair):
        pass

    def get_maxbid(self, pair):
        pass

    def get_balanses(self):
        pass

    def get_openorders(self):
        pass

    def get_partiallyorders(self):
        d = []
        return d

    def cancel_orders(self, order_ids):
        pass

    def buy_currency(self, pair, quantity, price):
        pass

    def sell_currency(self, pair, quantity, price):
        pass

    def get_buy_price(self, pair):
        pass

    def get_min_order_size(self, mult):
        return 0.0001 * mult

    def post_request(self, method, data):
        pass

    def get_best_bid(self, pair):
        pass

    def get_best_ask(self, pair):
        pass

    def get_btc_ex(self, cur):
        return cur + '/BTC'

    def get_btc_balance(self, balance):
        if 'BTC' in balance:
            return balance['BTC']
        else:
            return 0
