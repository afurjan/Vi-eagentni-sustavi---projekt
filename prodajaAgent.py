import asyncio
import os
from binance.client import Client
from binance import ThreadedWebsocketManager
import pprint
import time
from matplotlib.pyplot import cla
from spade import agent, quit_spade
from spade.behaviour import OneShotBehaviour 
import spade

TEST_NET = True
class ProdajaAgent(spade.agent.Agent):
    class Prodaj(OneShotBehaviour):
        async def sell_ETH_at_BTC(self):
            try:
                print("Selling when BTCUSDT price:",self.btc['price'])
                order = self.client.order_market_sell(symbol='ETHUSDT', quantity=1)
                print(f"Prodajem ETH")
                pprint.pprint(order)
                
            except Exception as e:
                print(e)

        async def on_start(self):
            if TEST_NET:
                api_key = "D8F1i8zFCtbgCCVL1iHRDqlc7AN4Yt2xb3vDC1C1fboXmAs45esqz1x74VKlhHJF"
                api_secret = "w8IU6EaitCEX5wkNpXtGjBO2RkQigtaG4u1uuxjwqjPEH8PwJbTSuQBkTqsmSA2L"
                self.client = Client(api_key, api_secret, testnet=True)

        async def run(self):
            self.btc = self.client.get_symbol_ticker(symbol="BTCUSDT")
           
            if self.btc:
                print(f"{self.btc['symbol']}: {self.btc['price']} ")
                await self.sell_ETH_at_BTC()
            self.kill()
        
        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        behav = self.Prodaj()
        self.add_behaviour(behav)
