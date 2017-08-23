from basebot import abstract_api
import requests
import json
import hmac
import hashlib
from livecoin_api.skeys import client_key
from livecoin_api.skeys import client_secret
from urllib.parse import urlencode
from collections import OrderedDict
import http.client

ex_url = 'https://api.livecoin.net/'
server = 'api.livecoin.net'

class trade_api(abstract_api):
    def __init__(self, proxy_sett):
        self.proxy = proxy_sett['proxy_url']
        self.proxyhost = proxy_sett['proxyhost']
        self.proxyport = proxy_sett['proxyport']
        self.proxy_used = proxy_sett['proxy_used']
        self.proxyDict = proxy_sett['proxyDict']

    def tr_query(self, url):
        if self.proxy_used:
            req = requests.get(url, proxies=self.proxyDict)
        else:
            req = requests.get(url)
        return json.loads(req.text)

    def get_request(self, method, data):
        encoded_data = urlencode(data)
        sign = hmac.new(client_secret.encode(), msg=encoded_data.encode(), digestmod=hashlib.sha256).hexdigest().upper()
        headers = {"Api-key": client_key, "Sign": sign}
        if self.proxy_used:
            conn = http.client.HTTPSConnection(self.proxyhost, self.proxyport)
            conn.set_tunnel(server)
        else:
            conn = http.client.HTTPSConnection(server)
        conn.request("GET", method + '?' + encoded_data, '', headers)
        response = conn.getresponse().read().decode('utf-8')
        conn.close()
        return response

    def post_request(self, method, data):
        encoded_data = urlencode(data)
        sign = hmac.new(client_secret.encode(), msg=encoded_data.encode(),
                        digestmod=hashlib.sha256).hexdigest().upper()
        headers = {"Api-key": client_key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
        if self.proxy_used:
            conn = http.client.HTTPSConnection(self.proxyhost, self.proxyport)
            conn.set_tunnel(server)
        else:
            conn = http.client.HTTPSConnection(server)
        conn.request("POST", method, encoded_data, headers)
        response = conn.getresponse().read().decode('utf-8')
        conn.close()
        return response

    def get_coin_list(self):
        return self.tr_query(ex_url + '/exchange/ticker')

    def get_down_list(self):
        d = []
        lst = self.tr_query(ex_url + '/info/coinInfo')
        for co in lst['info']:
            if co['walletStatus'] != 'normal':
                d.append(co['symbol'])
        return d

    def get_coin_details(self, pair):
        return self.tr_query(ex_url + '/exchange/maxbid_minask/?currencyPair=' + pair)

    def get_volume(self, co):
        return float(co['volume']) * float(co['last'])

    def is_btc(self, pair):
        return '/BTC' in pair

    def get_pair(self, pair):
        return pair['symbol']

    def get_low(self, pair):
        return pair['low']

    def get_high(self, pair):
        return pair['high']

    def get_best_bid(self, pair):
        return pair['best_bid']

    def get_best_ask(self, pair):
        return pair['best_ask']

    def is_Error(self, req):
        return 'errorCode' in req

    def get_currency_info(self, req):
        return req['currencyPairs'][0]

    def get_minask(self, pair):
        return float(pair['minAsk'])

    def get_maxbid(self, pair):
        return float(pair['maxBid'])

    def get_balanses(self):
        method = '/payment/balances'
        data = OrderedDict([])
        response = self.get_request(method, data)
        d = json.loads(response)
        balances = {}
        for cu in d:
            if ('None' not in str(cu['value'])):
                if (cu['value'] > 0):
                    if cu['currency'] not in balances:
                        balances[cu['currency']] = cu['value']

        return balances

    def get_openorders(self):
        method = '/exchange/client_orders'
        data = OrderedDict(sorted([('openClosed', 'OPEN')]))
        response = self.get_request(method, data)
        d = json.loads(response)
        order_ids = []
        if d['totalRows'] > 0:
            d = d['data']
            for od in d:
                if od['orderStatus'] == 'OPEN':
                    order_ids.append({'pair': od['currencyPair'], 'id': od['id']})
        return order_ids

    def get_partiallyorders(self):
        method = '/exchange/client_orders'
        data = OrderedDict(sorted([('openClosed', 'PARTIALLY')]))
        response = self.get_request(method, data)
        d = json.loads(response)
        order_pairs = []
        if d['totalRows'] > 0:
            d = d['data']
            for od in d:
                if od['orderStatus'] == 'PARTIALLY_FILLED':
                    order_pairs.append(od['currencyPair'])
                if od['orderStatus'] == 'PARTIALLY':
                    order_pairs.append(od['currencyPair'])
        return order_pairs

    def get_buy_price(self, pair):
        '''
            Выдать цену покупки имеющеёся вылюты
        :param pair:
        :return: float
        '''
        method = '/exchange/trades'
        data = OrderedDict(sorted([('currencyPair', pair)]))
        response = self.get_request(method, data)
        d = json.loads(response)
        if 'success' in d:
            if d['success'] == False:
                return 0
        sum = 0
        for tr in d:
            if tr['type'] == 'sell':
                break
            else:
                sum = tr['price']
        return sum

    def cancel_orders(self, order_ids):
        method = "/exchange/cancellimit"
        for od in order_ids:
            data = OrderedDict(sorted([('currencyPair', od['pair']), ('orderId', od['id'])]))
            response = self.post_request(method, data)
            value = json.loads(response)
            if value['cancelled'] == True:
                print('успешно отменен ордер #', od['id'], 'объёмом', value['quantity'], od['pair'])
            else:
                print('ошибка отмены ордера #', od['id'], od['pair'])

    def buy_currency(self, pair, quantity, price):
        method = "/exchange/buylimit"
        data = OrderedDict(sorted([('currencyPair', pair), ('price', price), ('quantity', quantity)]))
        response = self.post_request(method, data)
        value = json.loads(response)
        if value['success'] == True:
            print('успешно создан ордер на покупку', str(quantity), pair, 'по курсу', str(price), ' #:',
                  value['orderId'])
        else:
            print(value)

    def sell_currency(self, pair, quantity, price):
        method = "/exchange/selllimit"
        data = OrderedDict(sorted([('currencyPair', pair), ('price', price), ('quantity', quantity)]))
        response = self.post_request(method, data)
        value = json.loads(response)
        if value['success'] == True:
            print('успешно создан ордер на продажу', str(quantity), pair, 'по курсу', str(price), ' #:',
                  value['orderId'])
        else:
            print(value)
