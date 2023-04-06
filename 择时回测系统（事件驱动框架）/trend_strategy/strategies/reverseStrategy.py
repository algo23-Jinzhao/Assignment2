from trend_strategy import TrendTemplate

class ReverseStrategy(TrendTemplate):
    def __init__(self, initial_data) -> None:
        super(ReverseStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:list) -> list:
        df2 = self.df2
        reverse_window = parameters
        back_return = (df2['close'].shift() / df2['close'].shift(2) - 1).rolling(reverse_window).mean()

        signal = [0]*reverse_window
        for i in range(reverse_window, len(back_return)):
            if back_return[i] < 0: 
                signal.append(1)
            elif back_return[i] > 0: 
                signal.append(-1)
            else:
                signal.append(signal[-1]) # 跟随趋势
        return signal