from strategyTemplate import BasicStrategy

class PreTrendStrategy(BasicStrategy):
    def __init__(self, initial_data) -> None:
        super(PreTrendStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:int) -> list:
        window = parameters
        pre_return = self.df2['close'].shift(-window) / self.df2['close'] - 1
        signal = []
        for i in range(len(pre_return)-window):
            if pre_return[i] > 0: 
                signal.append(1)
            else: 
                signal.append(-1)
        signal.append(-1)
        return signal