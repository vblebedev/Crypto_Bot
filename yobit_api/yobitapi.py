import requests
import json
import hmac
import time
import hashlib
from yobit_api import client_key
from yobit_api import client_secret
from urllib.parse import urlencode


proxy = 'proxy.ru:3128'

proxyDict = {
    "http": proxy,
    "https": proxy,
    "ftp": proxy
}


def yo_query(method, values):
    md_public = ['info', 'ticker', 'depth', 'trades']

    if method in md_public:
        url = 'https://yobit.net/api/3/' + method
        for k in values:
            if (k == 'currency') and (values[k] != ''):
                url += '/' + values[k]
        for k in values:
            if (k != 'currency') and (values[k] != ''):
                url += '?' + k + '=' + values[k]

        req = requests.get(url, proxies=proxyDict)
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

        req = requests.post(url, data=values, headers=headers, proxies=proxyDict)
        return json.loads(req.text)


# PUBLIC API
# ---------------------------------------------------------------------------------------------------------------------
# Информация обо всех парах
def getinfo():
    return yo_query('info', {})


# Информация по паре
def getticker(currency):
    return yo_query('ticker', {'currency': currency})


# Состояние торгов
def getdepth(currency):
    return yo_query('depth', {'currency': currency})


# История сделок
def gettrades(currency, limit=150):
    return yo_query('trades', {'currency': currency, 'limit': str(limit)})


# ---------------------------------------------------------------------------------------------------------------------


# TRADE API
# ---------------------------------------------------------------------------------------------------------------------

# getInfo
def getfunds():
    return yo_query('getInfo', {})


# Trade
def trade(pair, ttype, rate, amount):
    return yo_query('Trade', {'pair': pair, 'type': ttype, 'rate': rate, 'amount': amount})


# ActiveOrders
def getactiveorders(pair):
    return yo_query('ActiveOrders', {'pair': pair})


# OrderInfo
def getorderinfo(order_id):
    return yo_query('OrderInfo', {'order_id': order_id})


# CancelOrder
def cancelorder(order_id):
    return yo_query('CancelOrder', {'order_id': order_id})


# TradeHistory
def gettradehistory(pair, from_n=0, count=1000, from_id=0, end_id='', order='DESC', since=0, end=''):
    return yo_query('TradeHistory',
                    {'from': from_n, 'count': count, 'from_id': from_id, 'end_id': end_id, 'order': order,
                     'since': since, 'end': end, 'pair': pair})


# GetDepositAddress
def getdepositaddress(coinname, is_need_new=0):
    return yo_query('GetDepositAddress', {'coinName': coinname, 'need_new': is_need_new})


# WithdrawCoinsToAddress
def withdrawcoinstoaddress(coinname, amount, address):
    return yo_query('WithdrawCoinsToAddress', {'coinName': coinname, 'amount': amount, 'address': address})

# ---------------------------------------------------------------------------------------------------------------------
