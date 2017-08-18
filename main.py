from livecoin_api import trade_api
import settings

trade_bot = trade_api()

order_ids = trade_bot.get_openorders()

ex_list = trade_bot.get_partiallyorders()

trade_bot.cancel_orders(order_ids)

balances = trade_bot.get_balanses()
print(balances)

btc_balance = balances['BTC']

for b in balances:
    if b != 'BTC':
        ex_list.append(b + '/BTC')
        # sell this currency
        buys_pr = trade_bot.get_buy_price(b + '/BTC')
        if (buys_pr) == 0:
            print('Не смог найти данные о покупке ' + b)
            continue
        dt = trade_bot.get_coin_details(b + '/BTC')
        if not trade_bot.is_Error(dt):
            dt = trade_bot.get_currency_info(dt)
            min_ask = trade_bot.get_minask(dt) - settings.sell_step
            if buys_pr * (1 + settings.min_delta + 0.005) < min_ask:
                trade_bot.sell_currency(b + '/BTC', "{0:.8f}".format(balances[b]), "{0:.8f}".format(min_ask))
            else:
                print('Прогорели в ' + b)

ex_list.append('MCO/BTC')
ex_list.append('BCH/BTC')

order_size = trade_bot.get_min_order_size(settings.min_order_mult)
max_num_orders = int(btc_balance / order_size)

pair_ls = trade_bot.get_coin_list()

d = {}

# get pair list for analisis
for co in pair_ls:
    vol = trade_bot.get_volume(co)
    sym = trade_bot.get_pair(co)
    lo = trade_bot.get_low(co)
    if (vol > settings.min_volume) and (lo > settings.min_ask) and trade_bot.is_btc(sym) and (sym not in ex_list):
        d[sym] = vol

rg_list = []

# get rang for all coins in list
for co in d:
    dt = trade_bot.get_coin_details(co)
    if not trade_bot.is_Error(dt):
        dt = trade_bot.get_currency_info(dt)
        min_ask = trade_bot.get_minask(dt)
        max_bid = trade_bot.get_maxbid(dt)
        pr = (min_ask - max_bid - settings.buy_step - settings.sell_step) / (max_bid + settings.buy_step)
        rang = pr * d[co]
        if (pr > settings.min_profit) and (pr < settings.max_profit):
            rg_list.append({'rang': rang, 'symbol': trade_bot.get_pair(dt)})

rg_list.sort(key=lambda i: i['rang'], reverse=True)

if max_num_orders > len(rg_list):
    max_num_orders = len(rg_list)
    order_size = btc_balance / max_num_orders

i = 0
for k in rg_list:
    if i < max_num_orders:
        dt = trade_bot.get_coin_details(k['symbol'])
        if not trade_bot.is_Error(dt):
            dt = trade_bot.get_currency_info(dt)
            max_bid = trade_bot.get_maxbid(dt) + settings.buy_step
            quantity = order_size/max_bid
            while (quantity > 0.00000001) and ((quantity*max_bid) > order_size):
                quantity -= 0.00000001
            print(k['symbol'], "{0:.8f}".format(quantity), "{0:.8f}".format(max_bid), k['rang'])
            trade_bot.buy_currency(k['symbol'], "{0:.8f}".format(quantity), "{0:.8f}".format(max_bid))
    else:
        break
    btc_balance -= order_size
    if btc_balance < order_size:
        order_size = btc_balance
    i += 1
