from trend_strategy import TrendTemplate

class BackTrendStrategy(TrendTemplate):
    def __init__(self, initial_data) -> None:
        super(BackTrendStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:list) -> list:
        df2 = self.df2
        window = parameters
        back_return = (df2['close'].shift() / df2['close'].shift(2) - 1).rolling(window).mean()

        signal = [0]*window
        for i in range(window, len(back_return)):
            if back_return[i] > 0: 
                signal.append(1)
            elif back_return[i] < 0: 
                signal.append(-1)
            else:
                signal.append(signal[-1]) # 跟随趋势
        return signal