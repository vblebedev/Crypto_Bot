from basebot import abstract_api
import yobit_api


class trade_api(abstract_api):
    def get_openorders(self):
        d = []
        pr_lst = []
        fnd = yobit_api.getfunds()
        if fnd['success'] == 1:
            fnd = fnd['return']['funds_incl_orders']
        for f in fnd:
            if fnd[f] > 0:
                pr_lst.append(f)

        for pr in pr_lst:
            if pr != 'btc':
                try:
                    gto = yobit_api.getactiveorders(pr + self.get_btc_ex())
                    if gto['success'] == 1 and 'return' in gto:
                        for ao in gto['return']:
                            d.append(ao)
                except:
                    pass
        return d

    def get_btc_ex(self):
        return '_btc'

    def get_btc_balance(self, balance):
        if 'btc' in balance:
            return balance['btc']
        else:
            return 0

    def get_balanses(self):
        d = {}
        fnd = yobit_api.getfunds()
        if fnd['success'] == 1:
            fnd = fnd['return']['funds']
        for f in fnd:
            if fnd[f] > 0:
                d[f] = fnd[f]
        return d

    def cancel_orders(self, order_ids):
        for ods in order_ids:
            yobit_api.cancelorder(ods)

    def get_buy_price(self, pair):
        p = 0
        trs = yobit_api.gettradehistory(pair, count=1)
        if trs['success'] == 1 and ('return' in trs):
            trs = trs['return']
            for t in trs:
                if trs[t]['type'] == 'buy':
                    p = float(trs[t]['rate'])
                    break
        return p

    def get_coin_details(self, pair):
        return yobit_api.getticker(pair)

    def is_Error(self, req):
        return False

    def get_currency_info(self, req):
        for r in req:
            return req[r]

    def get_minask(self, pair):
        return pair['sell']

    def sell_currency(self, pair, quantity, price):
        return yobit_api.trade(pair, 'sell', price, quantity)

    def get_coin_list(self):
        rs = []
        d = yobit_api.getinfo()
        pair_list = []
        for pr in d['pairs']:
            if '_btc' in pr:
                pair_list.append(pr)
#        YoBit have nearly  a thousand coins. Most of them are shitcoins. So it makes sense to do the white list of coins     
#        pair_list = ['eth_btc', 'dash_btc', 'lsk_btc', 'waves_btc', 'edit_btc', 'nlc2_btc', 'ping_btc',
#                     'cube_btc', 'av_btc', 'bub_btc', 'plbt_btc', 'dgb_btc', 'ltc_btc', 'doge_btc', 'nlg_btc',
#                     'zec_btc', 'mcar_btc', 'etc_btc', 'zeni_btc', 'xby_btc', 'laz_btc', 'ent_btc',
#                     'game_btc', 'kgb_btc', 'max_btc', 'hmc_btc', 'mco_btc', 'ecob_btc', 'sak_btc', 'html5_btc',
#                     'clud_btc', 'rubit_btc', 'find_btc', 'pie_btc', 'icash_btc']
#

        for pr in pair_list:
            cd = self.get_coin_details(pr)
            cd = self.get_currency_info(cd)
            cd['pair'] = pr
            rs.append(cd)
        return rs

    def get_volume(self, co):
        return float(co['vol'])

    def is_btc(self, pair):
        return '_btc' in pair

    def get_pair(self, pair):
        return pair['pair']

    def get_low(self, pair):
        return pair['low']

    def get_high(self, pair):
        return pair['high']

    def get_best_bid(self, pair):
        return pair['buy']

    def get_maxbid(self, pair):
        return pair['buy']

    def get_best_ask(self, pair):
        return pair['sell']

    def buy_currency(self, pair, quantity, price):
        return yobit_api.trade(pair, 'buy', price, quantity)
