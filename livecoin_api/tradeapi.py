from basebot import abstract_api
import requests
import json

ex_url = 'https://api.livecoin.net/'

proxy = 'maker.garant.ru:3128'

proxyDict = {
    "http": proxy,
    "https": proxy,
    "ftp": proxy
}


def tr_query(url):
    req = requests.get(url, proxies=proxyDict)
    return json.loads(req.text)


class trade_api(abstract_api):
    def clear_orders(self):
        pass

    def get_coin_list(self):
        return tr_query(ex_url + '/exchange/ticker')

    def get_coin_details(self, pair):
        return tr_query(ex_url + '/exchange/maxbid_minask/?currencyPair=' + pair)

    def get_volume(self, co):
        return float(co['volume']) * float(co['last'])

    def is_btc(self, pair):
        return '/BTC' in pair

    def get_pair(self, pair):
        return pair['symbol']

    def get_low(self, pair):
        return pair['low']

    def is_Error(self, req):
        return 'errorCode' in req

    def get_currency_info(self, req):
       return req['currencyPairs'][0]

    def get_minask(self, pair):
        return float(pair['minAsk'])

    def get_maxbid(self, pair):
        return float(pair['maxBid'])
