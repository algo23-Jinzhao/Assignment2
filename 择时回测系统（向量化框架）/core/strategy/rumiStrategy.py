from template import BasicStrategy

class RUMIStrategy(BasicStrategy):
    def __init__(self, initial_data) -> None:
        super(RUMIStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:list) -> list:
        df2 = self.df2
        fast_window, slow_window = parameters

        sma = df2['close'].rolling(fast_window).mean().shift()
        lma = df2['close'].rolling(slow_window).mean().shift()
        ma_diff = sma - lma
        rumi_value = ma_diff.rolling(fast_window).mean()

        signal = [0]*slow_window
        for i in range(slow_window, len(df2.index)-1):
            if rumi_value[i] > 0: 
                signal.append(1)
            elif rumi_value[i] < 0:
                signal.append(-1)
            else:
                signal.append(signal[-1]) # 跟随趋势
        signal.append(-1)
        return signal