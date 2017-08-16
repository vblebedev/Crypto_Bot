from livecoin_api import trade_api
import settings

trade_bot = trade_api()

pair_ls = trade_bot.get_coin_list()

d = {}

# get pair list for analisis
for co in pair_ls:
    vol = trade_bot.get_volume(co)
    sym = trade_bot.get_pair(co)
    lo = trade_bot.get_low(co)
    if (vol > settings.min_volume) and (lo > settings.min_ask) and trade_bot.is_btc(sym):
        d[sym] = vol

rg_list = []

# get rang for all coins in list
for co in d:
    dt = trade_bot.get_coin_details(co)
    if not trade_bot.is_Error(dt):
        dt = trade_bot.get_currency_info(dt)
        min_ask = trade_bot.get_minask(dt)
        max_bid = trade_bot.get_maxbid(dt)
        pr = (min_ask - max_bid - 0.00000002) / (max_bid + 0.00000001)
        rang = pr * d[co]
        if (pr > settings.min_profit) and (pr < settings.max_profit):
            rg_list.append({'rang': rang, 'symbol': trade_bot.get_pair(dt)})

rg_list.sort(key=lambda i: i['rang'], reverse=True)

for k in rg_list:
    print(k['symbol'], k['rang'])
