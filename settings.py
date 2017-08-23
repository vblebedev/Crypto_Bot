default_loss_time = 14  # in days
min_volume = 2  # min volume
min_ask = 0.000005  # min ask
min_profit = 0.04
max_profit = 0.3
min_delta = 0.02
min_order_mult = 1.5
buy_step = 0.00000001
sell_step = 0.00000001
max_dev = 0.25

proxy = 'maker.garant.ru:3128'
proxyhost = 'maker.garant.ru'
proxyport = 3128
proxy_used = True

proxyDict = {
    "http": proxy,
    "https": proxy,
    "ftp": proxy
}

proxy_sett = {
    'proxy_url': proxy,
    'proxyhost': proxyhost,
    'proxyport': proxyport,
    'proxy_used': proxy_used,
    'proxyDict': proxyDict

}
