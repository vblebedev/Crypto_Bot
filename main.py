from livecoin_api import trade_api
import settings

trade_bot = trade_api(settings.proxy_sett)

order_ids = trade_bot.get_openorders()

ex_list = trade_bot.get_partiallyorders()
print(ex_list)
down_list = trade_bot.get_down_list()

for dl in down_list:
    ex_list.append(dl + trade_bot.get_btc_ex())

ex_list.append('BCH' + trade_bot.get_btc_ex())

trade_bot.cancel_orders(order_ids)

balances = trade_bot.get_balanses()
print(balances)

btc_balance = trade_bot.get_btc_balance(balances)

for b in balances:
    if str(b).upper() != 'BTC' and ((b + trade_bot.get_btc_ex()) not in ex_list):
        ex_list.append(b + trade_bot.get_btc_ex())
        # sell this currency
        buys_pr = trade_bot.get_buy_price(b + trade_bot.get_btc_ex())
        if (buys_pr) == 0:
            print('Не смог найти данные о покупке ' + str(b).upper())
            continue
        dt = trade_bot.get_coin_details(b + trade_bot.get_btc_ex())
        if not trade_bot.is_Error(dt):
            dt = trade_bot.get_currency_info(dt)
            min_ask = trade_bot.get_minask(dt) - settings.sell_step
            if buys_pr * (1 + settings.min_delta) < min_ask:
                trade_bot.sell_currency(b + trade_bot.get_btc_ex(), "{0:.8f}".format(balances[b]), "{0:.8f}".format(min_ask))
            else:
                print('Прогорели в ' + b)

order_size = trade_bot.get_min_order_size(settings.min_order_mult)
max_num_orders = int((btc_balance * 0.99) / order_size)

pair_ls = trade_bot.get_coin_list()

rg_list = []

# get pair list for analisis
for co in pair_ls:
    vol = trade_bot.get_volume(co)
    sym = trade_bot.get_pair(co)
    low = trade_bot.get_low(co)
    high = trade_bot.get_high(co)
    best_bid = trade_bot.get_best_bid(co)
    best_ask = trade_bot.get_best_ask(co)
    if high > low:
        dev = (high - low) / low
    else:
        dev = settings.max_dev
    if (vol > settings.min_volume) and (low > settings.min_ask) and trade_bot.is_btc(sym) and (sym not in ex_list) and (
                dev < settings.max_dev):
        pr = (best_ask - best_bid - settings.buy_step - settings.sell_step) / (best_bid + settings.buy_step)
        rang = pr * vol
        if (pr > settings.min_profit) and (pr < settings.max_profit):
            rg_list.append({'rang': rang, 'symbol': sym})

rg_list.sort(key=lambda i: i['rang'], reverse=True)

if max_num_orders > len(rg_list):
    max_num_orders = len(rg_list)
    order_size = (btc_balance * 0.99) / max_num_orders

    while (order_size * max_num_orders) > (btc_balance * 0.99):
        order_size -= 0.00000001

i = 0
for k in rg_list:
    if i < max_num_orders:
        dt = trade_bot.get_coin_details(k['symbol'])
        if not trade_bot.is_Error(dt):
            dt = trade_bot.get_currency_info(dt)
            max_bid = trade_bot.get_maxbid(dt) + settings.buy_step
            quantity = order_size / max_bid
            trade_bot.buy_currency(k['symbol'], "{0:.8f}".format(quantity), "{0:.8f}".format(max_bid))
    else:
        break
    btc_balance -= order_size
    if btc_balance < order_size:
        order_size = btc_balance
    i += 1
