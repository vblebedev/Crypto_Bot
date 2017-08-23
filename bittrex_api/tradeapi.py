from basebot import abstract_api
import bittrex_api


class trade_api(abstract_api):
    def __init__(self, proxy_sett):
        self.proxy_settings = proxy_sett
        self.bittrex = bittrex_api.Bittrex(proxy_sett)
