import os
import time
import MetaTrader5 as mt5

symbol = "EURUSD"
points_range = [10, 1200, 2000, 5000, 8000]

def get_symbol_values(symbol_info_dict):
    point = symbol_info_dict.get('point')
    trade_tick_value_profit = symbol_info_dict.get('trade_tick_value_profit')
    trade_tick_value_loss = symbol_info_dict.get('trade_tick_value_loss')
    volume_min = symbol_info_dict.get('volume_min')

    profit_values: list[float] = []
    loss_values: list[float] = []

    for point_diff in points_range:
        calc_profit = point_diff * trade_tick_value_profit * volume_min
        calc_loss = point_diff * trade_tick_value_loss * volume_min

        profit_values.append(calc_profit)
        loss_values.append(calc_loss)

    print(f"\n{symbol} - Volume (lot size): {volume_min}")
    print("\tProfit Values: \t\t\tLoss Values:")
    for i in range(len(points_range)):
        print(f'\t{points_range[i]} points: USD {profit_values[i]:,.2f}\t\t{points_range[i]} points: USD {loss_values[i]:,.2f}')
    print()

if __name__ == "__main__":
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        mt5.shutdown()
    
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print("Symbol not found...")
        print("MT5 connection closed")
        mt5.shutdown()
    else:
        try:
            while True:
                os.system('cls')

                symbol_info_dict = symbol_info._asdict()
                get_symbol_values(symbol_info_dict)
                time.sleep(1)

                symbol_info = mt5.symbol_info(symbol)
        except KeyboardInterrupt:
            mt5.shutdown()
            print("MT5 connection closed")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            mt5.shutdown()
            print("MT5 connection closed")
  
  
