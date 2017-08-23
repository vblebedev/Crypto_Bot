import requests
import json
import hmac
import time
import hashlib
from yobit_api import client_key
from yobit_api import client_secret
from urllib.parse import urlencode

class Yobit(object):
    def __init__(self, proxy_sett):
        self.proxy_settings = proxy_sett

    def yo_query(self, method, values):
        md_public = ['info', 'ticker', 'depth', 'trades']

        if method in md_public:
            url = 'https://yobit.net/api/3/' + method
            for k in values:
                if (k == 'currency') and (values[k] != ''):
                    url += '/' + values[k]
            for k in values:
                if (k != 'currency') and (values[k] != ''):
                    url += '?' + k + '=' + values[k]
            if self.proxy_settings['proxy_used']:
                req = requests.get(url, proxies=self.proxy_settings['proxyDict'])
            else:
                req = requests.get(url)
            return json.loads(req.text)

        else:
            url = 'https://yobit.net/tapi'
            values['method'] = method
            values['nonce'] = str(int(time.time()))
            body = urlencode(values)
            signature = hmac.new(client_secret, body.encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': client_key,
                'Sign': signature
            }
            if self.proxy_settings['proxy_used']:
                req = requests.post(url, data=values, headers=headers, proxies=self.proxy_settings['proxyDict'])
            else:
                req = requests.post(url, data=values, headers=headers)
            return json.loads(req.text)


    # PUBLIC API
    # ---------------------------------------------------------------------------------------------------------------------
    # Информация обо всех парах
    def getinfo(self):
        return self.yo_query('info', {})


    # Информация по паре
    def getticker(self, currency):
        return self.yo_query('ticker', {'currency': currency})


    # Состояние торгов
    def getdepth(self, currency):
        return self.yo_query('depth', {'currency': currency})


    # История сделок
    def gettrades(self, currency, limit=150):
        return self.yo_query('trades', {'currency': currency, 'limit': str(limit)})


    # ---------------------------------------------------------------------------------------------------------------------


    # TRADE API
    # ---------------------------------------------------------------------------------------------------------------------

    # getInfo
    def getfunds(self):
        return self.yo_query('getInfo', {})


    # Trade
    def trade(self, pair, ttype, rate, amount):
        return self.yo_query('Trade', {'pair': pair, 'type': ttype, 'rate': rate, 'amount': amount})


    # ActiveOrders
    def getactiveorders(self, pair):
        return self.yo_query('ActiveOrders', {'pair': pair})


    # OrderInfo
    def getorderinfo(self, order_id):
        return self.yo_query('OrderInfo', {'order_id': order_id})


    # CancelOrder
    def cancelorder(self, order_id):
        return self.yo_query('CancelOrder', {'order_id': order_id})


    # TradeHistory
    def gettradehistory(self, pair, from_n=0, count=1000, from_id=0, end_id='', order='DESC', since=0, end=''):
        return self.yo_query('TradeHistory',
                        {'from': from_n, 'count': count, 'from_id': from_id, 'end_id': end_id, 'order': order,
                         'since': since, 'end': end, 'pair': pair})


    # GetDepositAddress
    def getdepositaddress(self, coinname, is_need_new=0):
        return self.yo_query('GetDepositAddress', {'coinName': coinname, 'need_new': is_need_new})


    # WithdrawCoinsToAddress
    def withdrawcoinstoaddress(self, coinname, amount, address):
        return self.yo_query('WithdrawCoinsToAddress', {'coinName': coinname, 'amount': amount, 'address': address})

    # ---------------------------------------------------------------------------------------------------------------------
