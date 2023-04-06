import pandas as pd

class Engine:
    pass

class DataEngine(Engine):
    def __init__(self, stock_name) -> None:
        self.df = pd.read_csv(stock_name)
    def load_bar(self, days):
        pass

class OrderEngine(Engine):
    pass