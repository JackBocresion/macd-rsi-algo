from datetime import datetime
from lumibot.backtesting import PolygonDataBacktesting
from lumibot.strategies import Strategy
from pandas import DataFrame
from lumibot.entities import Asset
import pandas_ta
from math import floor
class MyStrategy(Strategy):
    parameters = {
        "symbol": "SPY",
    }
    data=[]
    
    # self.set_market("24/7") # for a crypto market 


    def initialize(self):
        self.sleeptime = "1M"
    def on_trading_iteration(self):
    #     if self.first_iteration:
    #         aapl_price = self.get_last_price(symbol)
    #         quantity = self.portfolio_value // aapl_price
    #         order = self.create_order(symbol, quantity, "buy")
    #         self.submit_order(order)
        
        
        
        symbol = self.parameters["symbol"]
        minbars=self.get_historical_prices(symbol, 200, "minute")
        # daybars=self.get_historical_prices(symbol, 200, "day")
        df=minbars.df
        rsi = df.ta.rsi(length=20)
        current_rsi = rsi.iloc[-1]
        last_rsi = rsi.iloc[-2] # 1 minute ago
        self.log_message(f"RSI was {current_rsi}")

        # Use pandas_ta to calculate the MACD
        macd = df.ta.macd()
        current_macd = macd.iloc[-1]
        last_macd = macd.iloc[-2] # 1 minute ago
        # self.log_message(f"MACD for {base} was {current_macd}") #h=histogram, macd=macd line, s=signal lime

        # Use pandas_ta to calculate the 55 EMA
        ema = df.ta.ema(length=100)
        current_ema = ema.iloc[-1]
        self.log_message(f"EMA was {type(current_ema)}")
        price = self.get_last_price(symbol)
        # current_ema < price and
        # 
        if current_macd["MACDh_12_26_9"]>0 and self.get_position(symbol)==None and current_rsi<30 and (last_macd["MACDh_12_26_9"]<0 or last_rsi>60):
            qty=floor(self.cash/price)
            self.log_message(f"BUYING")
            # stop_loss_price=0.98*price,
            order = self.create_order(symbol, qty, "buy", take_profit_price=1.03*price)
            self.submit_order(order)
        if current_macd["MACDh_12_26_9"]<0 and self.get_position(symbol)==None and current_rsi>70 and (last_macd["MACDh_12_26_9"]>0 or last_rsi<70):
            qty=floor(self.cash/price)
            self.log_message(f"SHORTING")
            # stop_loss_price=0.98*price,
            # stop_loss_price=1.1*price,
            order = self.create_order(symbol, qty, "sell",  take_profit_price=0.97*price) # add stop loss for shorts
            self.submit_order(order)
        # if self.get_datetime()==datetime(2023, 4, 30):
        #     self.sell_all()


if __name__ == "__main__":
    backtesting_start = datetime(2022, 5, 1)
    backtesting_end = datetime(2023, 5, 1)

    MyStrategy.backtest(
        PolygonDataBacktesting,
        backtesting_start,
        backtesting_end,
        polygon_api_key="d2tMM6GGzHaL_fFJrRlu09LJAeBmGCDz",
        polygon_has_paid_subscription=True,
        budget=1000
    )