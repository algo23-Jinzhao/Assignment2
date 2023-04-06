from abc import ABC, abstractmethod
from engine import DataEngine

class Template(ABC):
    def __init__(self, stock_name) -> None:
        self.dataengine = DataEngine(stock_name)

    @abstractmethod
    def on_bar(self):
        pass

    def buy(self):
        return 1

    def sell(self):
        return -1

    def send_signal(self, signal):
        return signal
    
    def load_bar(self, date, days):
        bars = self.dataengine.load_bar(date, days) # 订阅date近days天的行情
        for bar in bars:
            self.on_bar(bar)