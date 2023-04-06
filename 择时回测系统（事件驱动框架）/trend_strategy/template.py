from abc import ABC, abstractmethod
import pandas as pd

class TrendTemplate(ABC):
    parameters: list = []
    variables: list = []

    def __init__(self, strategy_name: str) -> None:
        self.strategy_name: str = strategy_name
        self.pos: int = 0
    
    @classmethod
    def get_default_parameters(cls) -> dict:
        """
        Get default parameters dict of strategy class.
        """
        class_parameters: dict = {}
        for name in cls.parameters:
            class_parameters[name] = getattr(cls, name)
        return class_parameters

    def get_parameters(self) -> dict:
        """
        Get strategy parameters dict.
        """
        strategy_parameters: dict = {}
        for name in self.parameters:
            strategy_parameters[name] = getattr(self, name)
        return strategy_parameters

    def get_variables(self) -> dict:
        """
        Get strategy variables dict.
        """
        strategy_variables: dict = {}
        for name in self.variables:
            strategy_variables[name] = getattr(self, name)
        return strategy_variables
    
    def get_strategy_data(self) -> dict:
        strategy_data: dict = {
            "strategy_name": self.strategy_name,
            "class_name": self.__class__.__name__,
            "parameters": self.get_parameters(),
            "variables": self.get_variables(),
        }
        return strategy_data
    
    @abstractmethod
    def on_bar(self) -> None:
        """
        Callback of new bar data update.
        """
        pass

    def load_bar(
        self,
        days: int,
        use_database: bool = False
    ) -> None:
        """
        Load historical bar data for initializing strategy.
        """
        pass

    def buy(
        self, 
        price: float,
        volume: float,
    ) -> list:
        """
        Send buy order to open a long position.
        """
        return self.send_order(
            price,
            volume
        )

    def sell(
        self,
        price: float,
        volume: float
    ) -> list:
        """
        Send sell order to close a long position.
        """
        return self.send_order(
            price,
            volume
        )

    def send_order(
        self,
        price: float,
        volume: float
    ) -> list:
        self.trendEngine(price, volume)

# data->signal
class TrendSignal(ABC):
    @abstractmethod
    def on_bar(self) -> list:
        pass
    
    # 设置信号
    def set_signal_pos(self, pos) -> None:
        self.signal_pos = pos

    # 获取信号
    def get_signal_pos(self):
        return self.signal_pos
    
    def get_pre_return():
        pre_return = (df2['close'].shift(-1) / df2['close'] - 1).fillna(0)
        df2['flag_pre'] = [1 if i > 0 else -1 for i in pre_return.values]

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

# signal->order
class TargetPosTemplate(TrendTemplate):
    last_bar: BarData = None
    target_pos = 0

    def on_bar(self) -> None:
        pass

    def on_value(self) -> None:
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

    def set_target_pos(self, target_pos) -> None:
        self.target_pos = target_pos
        self.trade()

    def send_order(self, last_pos, target_pos) -> tuple: 
        # 不考虑涨跌停
        # 进行开平仓操作
        if last_pos < target_pos:
            buy(close_price, target_pos-last_pos)
        elif last_pos > target_pos:
            sell(close_price, target_pos-last_pos)