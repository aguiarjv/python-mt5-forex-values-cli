import time
import os
import MetaTrader5 as mt5

class ForexSymbol:
    def __init__(self, symbol: str) -> None:
        self.symbol: str = symbol
        self.standard_lot_currency_units: int = 100000
        self.info_dict: dict[str, str | float | None] = {"currency_profit": None, "volume_min": None, 
                                                        "point": None, "bid": None, "ask": None, 
                                                        "trade_tick_value": None, "trade_tick_value_profit": None, "trade_tick_value_loss": None }
        self.points_range: list[int] = [10, 30, 60, 90, 120]

    def __str__(self) -> str:
        return self.symbol

    def get_symbol(self) -> str:
        return self.symbol
       
    def get_info(self) -> None:
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info != None:
            symbol_info_dict = symbol_info._asdict()
            for key in self.info_dict:
                self.info_dict[key] = symbol_info_dict.get(key)
    
    def print_all_info(self) -> None:
        for k, v in self.info_dict.items():
            print(f'{k} = {v}')

    def update_bid(self, bid: float) -> None:
        self.info_dict['bid'] = bid

    def update_ask(self, ask: float) -> None:
        self.info_dict['ask'] = ask

    def update_points_range(self, points_range: list[int]) -> None:
        self.points_range = points_range

    def trade_values(self, calculate: bool = False) -> None:
        """
        This method calculates the profit/loss values considering the 'self.points_range' list.

        By default this method will always consider that the symbol is a Forex currency pair
        and will use the 'trade_tick_value' from MT5 to calculate the values.

        This is not the best approach since using 'trade_tick_value' will result in wrong values, but
        it is a good approximation. By setting 'calculate' to True, this method will be more accurate.
        """

        profit_values: list[float] = []
        loss_values: list[float] = []

        
        if calculate:
            self.__calculate_trade_values(profit_values, loss_values)
        else:
            self.__ttv_trade_values(profit_values, loss_values)

        print("\tProfit Values:\t\t\tLoss Values:")
        for i in range(len(self.points_range)):
            print(f"\t{self.points_range[i]} points: USD {profit_values[i]:,.2f}\t\t{self.points_range[i]} points: USD {loss_values[i]:,.2f}")


    def __calculate_trade_values(self, profit_values: list[float], loss_values: list[float]) -> None:
        """
        This private method was created to be used with forex pairs that does not have the 'currency_profit' as USD.
        So it will calculate the profit/loss values based on the 'self.points_range' list and on the ASK price.
        """

        for point_diff in self.points_range:
            calc = point_diff * self.standard_lot_currency_units * self.info_dict['point'] * self.info_dict['volume_min'] 

            profit = calc / (self.info_dict['ask'] + point_diff*self.info_dict['point'])
            loss = calc / (self.info_dict['ask'] - point_diff*self.info_dict['point'])

            profit_values.append(profit)
            loss_values.append(loss)


    def __ttv_trade_values(self, profit_values: list[float], loss_values: list[float]) -> None:
        """
        This private method will calculate the profit/loss values based on the 'self.points_range' list
        and will use the 'trade_tick_value' from MT5. It is not the best calculation, but it is a fair
        approximation.
        """

        for point_diff in self.points_range:
            calc_profit = point_diff * self.info_dict['trade_tick_value_profit'] * self.info_dict['volume_min']
            calc_loss = point_diff * self.info_dict['trade_tick_value_loss'] * self.info_dict['volume_min']

            profit_values.append(calc_profit)
            loss_values.append(calc_loss)


def get_trade_values(symbol_objects_list: list[ForexSymbol]) -> None:

    while True:
        for symbol_object in symbol_objects_list:
            symbol_info_dict = mt5.symbol_info_tick(str(symbol_object))._asdict()

            ask = symbol_info_dict.get('ask')
            bid = symbol_info_dict.get('bid')

            if ask:
                symbol_object.update_ask(ask)

            if bid:
                symbol_object.update_ask(bid)

            print(str(symbol_object))
            symbol_object.trade_values(calculate=False)
            print()

        time.sleep(1)
        os.system('cls')
    
   
if __name__ == "__main__":
    os.system('cls')

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        mt5.shutdown()
    
    # List of symbols and points_range list
    symbols_list: list[list[str, list[int] | None]] = []
    symbols_list.append(["USDJPY", [30, 60, 150, 200, 500, 800]])
    symbols_list.append(["USDCHF", None])
    symbols_list.append(["USDCAD", None])

    symbol_objects_list: list[ForexSymbol] = []

    for symbol_info in symbols_list:
        symbol_objects_list.append(ForexSymbol(symbol_info[0]))
        symbol_objects_list[-1].get_info()

        if symbol_info[1]:
            symbol_objects_list[-1].update_points_range(symbol_info[1])

    try:
        get_trade_values(symbol_objects_list)
    except KeyboardInterrupt:
        mt5.shutdown()
        print("MT5 connection closed")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        mt5.shutdown()
        print("MT5 connection closed")
  









