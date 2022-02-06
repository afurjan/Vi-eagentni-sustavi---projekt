import asyncio
import os
from binance.client import Client
from binance import ThreadedWebsocketManager
import pprint
import time
from spade import agent, quit_spade
from spade.behaviour import CyclicBehaviour 
import spade
from prodajaAgent import ProdajaAgent

TEST_NET = True

class PrviAgent(spade.agent.Agent):
    class Kupnja(CyclicBehaviour):
        async def on_start(self):
            if TEST_NET:
                api_key = "D8F1i8zFCtbgCCVL1iHRDqlc7AN4Yt2xb3vDC1C1fboXmAs45esqz1x74VKlhHJF"
                api_secret = "w8IU6EaitCEX5wkNpXtGjBO2RkQigtaG4u1uuxjwqjPEH8PwJbTSuQBkTqsmSA2L"
                self.client = Client(api_key, api_secret, testnet=True)
                print("Koristi se TestNet server")

                for i in range(1, 2):
                    print("Ispis vremena racunala i binance servera:\n")
                    vrijeme_racunala = int(time.time() * 1000)
                    vrijeme_binance_servera = self.client.get_server_time()
                    razlika_vremena1 = vrijeme_binance_servera['serverTime'] - vrijeme_racunala
                    local_time2 = int(time.time() * 1000)
                    razlika_vremena2 = local_time2 - vrijeme_binance_servera['serverTime']
                    print("Racunalo: %s Server:%s Racunalo2: %s razlika_vremena1:%s razlika_vremena2:%s" % (vrijeme_racunala, vrijeme_binance_servera['serverTime'], local_time2, razlika_vremena1, razlika_vremena2))
                    time.sleep(2)
                    print("\n")

                self.kupljen = False
                self.btc_price = {'BTCUSDT': None, 'error': False}
              
               
                print("\n")
                pprint.pprint(self.client.get_account())
                print("Sadasnje stanje ETH-a Testnog Accounta:")
                print(self.client.get_asset_balance(asset='ETH'))
                print("\n")

        async def run(self):
        
            self.eth_price = self.client.get_symbol_ticker(symbol="ETHUSDT")
        
            self.btc = self.client.get_symbol_ticker(symbol="BTCUSDT")
           
            if self.btc:
                print(f"{self.btc['symbol']}: {self.btc['price']} ")
                await self.kupnja_ETH_na_cijeni_BTC()
                await asyncio.sleep(3)
        
        async def kupnja_ETH_na_cijeni_BTC(self):
         
            if float(najmanjaCijenaKupnje) < float(self.btc['price']) < float(najvecaCijenaKupnje) and self.kupljen == False: 
                try:
                    print("Kupnja ETH-a na sljedecoj cijeni BTCUSDT:",self.btc['price'])
                    print("Cijena ETH-a:",self.eth_price['price'])
                    print("\n")
                    print("Ispis detalja narudzbe: ")
                    order = self.client.order_market_buy(symbol='ETHUSDT', quantity=kolicinaKupnje)
                    pprint.pprint(order)
                    print("\n")
                    print(f"ETH je kupljen!")
                    self.kupljen = True
                    print("Sadasnje stanje ETH-a Testnog Accounta:")
                    print(self.client.get_asset_balance(asset='ETH'))
                       
                except Exception as e:
                    print("Nemate dovoljno sredstva (USDT-a) kako bi kupili ETH.")
                    
            if self.kupljen and float(self.btc['price']) > float(cijenaProdaje):
                prodajaAgent = ProdajaAgent("agent@rec.foi.hr","tajna")
                await prodajaAgent.start(auto_register=True)
                self.kupljen = False
    
    async def setup(self):
        kupnjaBehav = self.Kupnja()
        self.add_behaviour(kupnjaBehav)
  

if __name__ == "__main__":
    
    print("Kupnja:")
    najvecaCijenaKupnje=input("Unesite najvecu cijenu (BTC-a) do koje zelite kupiti: \n")
    najmanjaCijenaKupnje= input("Unesite najmanju cijenu kupnje (BTC-a) od koje zelite kupit: \n")
    kolicinaKupnje = input("Unesite kolicinu kriptovalute (ETH-a) koju zelite kupiti:\n")

    print("Prodaja:")
    cijenaProdaje= input("Unesite kada zelite prodat ETH: \n")

    a = PrviAgent("agent@rec.foi.hr", "tajna")
    a.start()
    print("Wait until user interrupts with ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    a.stop()
    quit_spade()