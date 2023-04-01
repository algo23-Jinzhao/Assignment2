from abc import ABC, abstractmethod
import pandas as pd

class BasicStrategy(ABC):
    def __init__(self, initial_data) -> None:
        self.df = initial_data
        self.df2 = pd.DataFrame()

    def class_name_str(self):
        return self.__class__.__name__

    # all data->core data
    def get_data(self) -> pd.DataFrame():
        df1 = self.df.copy()
        df1['date'] = pd.to_datetime(df1['date']).values.astype('datetime64[D]')
        df1.set_index('date', inplace=True)
        df2 = df1.loc['2012':, :].copy()
        pre_return = (df2['close'].shift(-1) / df2['close'] - 1).fillna(0)
        df2['flag_pre'] = [1 if i > 0 else -1 for i in pre_return.values]
        self.df2 = df2
        return self.df2
    
    # data->signal
    @abstractmethod
    def get_signal(self) -> list:
        pass

    def get_accurate_rate(self, result:list, calculate_days=60) -> float:
        # 比较一下准确率
        marked = list(self.df2['flag_pre'][calculate_days:])
        unmarked = result[calculate_days:].copy()
        right_times = 0
        n = len(unmarked)
        for i in range(n):
            if unmarked[i] == marked[i]:
                right_times += 1
        accurate_rate = right_times / n
        return round(accurate_rate, 4)

    # signal->order->net_values
    def get_trading(self, result:list, stop_win:float, stop_loss:float, calculate_days=60) -> tuple: 
        df2 = self.df2

        # 进行开平仓操作
        holding = False

        net_value_list = [1]*calculate_days
        unrealized_value_list = [1]*calculate_days
        net_value = 1
        unrealized_value = 1
        unit = 0
        for i in range(calculate_days, len(result)):
            if result[i] == 1 and holding == False:
                open_price = df2['close'][i]
                unit = net_value/open_price
                holding = True
            elif result[i] == -1 and holding == True:
                net_value = df2['close'][i]*unit # 平仓盈亏
                unrealized_value = net_value
                unit = 0
                holding = False
            elif unit > 0:
                unrealized_value = df2['close'][i]*unit # 浮动盈亏

                # 设置止盈止损
                if stop_win > 0:
                    if unrealized_value/net_value >= 1 + stop_win:
                        net_value = df2['close'][i]*unit # 平仓盈亏
                        unrealized_value = net_value
                        unit = 0
                        holding = False
                if stop_loss < 0:
                    if unrealized_value/net_value <= 1 + stop_loss:
                        net_value = df2['close'][i]*unit # 平仓盈亏
                        unrealized_value = net_value
                        unit = 0
                        holding = False
                
            net_value_list.append(net_value)
            unrealized_value_list.append(unrealized_value)
        
        stock_values = df2['close'][calculate_days:]/df2['close'][calculate_days]
        net_values = pd.Series(net_value_list[calculate_days:], index=stock_values.index)
        unrealized_values = pd.Series(unrealized_value_list[calculate_days:], index=stock_values.index)
        return stock_values, net_values, unrealized_values 
    
    # net_values->returns
    def get_returns(self, net_values, stock_values):
        strategy_returns = (net_values/net_values.shift()-1).fillna(0)
        benchmark_returns = (stock_values/stock_values.shift()-1).fillna(0)
        return strategy_returns, benchmark_returns