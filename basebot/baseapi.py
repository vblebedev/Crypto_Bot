class abstract_api():
    def clear_orders(self):
        pass

    def get_coin_list(self):
        pass

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

    def is_Error(self, req):
        return False

    def get_currency_info(self, req):
        pass

    def get_minask(self, pair):
        pass

    def get_maxbid(self, pair):
        pass
