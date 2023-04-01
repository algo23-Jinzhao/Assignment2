from trendStrategy import BasicStrategy

def LLT(data, d):
    llt = [(data[0]+data[1])/2, (data[0]+data[1])/2]
    alpha = 2/(d+1)
    for i in range(2, len(data)):
        llt.append((alpha-alpha**2/4)*data[i] + alpha**2/2*data[i-1] - (alpha-3*alpha**2/4)*data[i-2] \
            + 2*(1-alpha)*llt[i-1] - (1-alpha)**2*llt[i-2])
    return llt

def iterLLT(initial_data, d, n):
    data = initial_data
    for _ in range(n):
        data = LLT(data, d)
    return data

class LLTStrategy(BasicStrategy):
    def __init__(self, initial_data) -> None:
        super(LLTStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:list) -> list:
        # llt 的斜率
        df2 = self.df2
        llt_window = parameters

        llt_line = iterLLT(df2['close'], llt_window, 1)

        signal = [0]*llt_window
        for i in range(llt_window+1, len(df2.index)):
            if llt_line[i-1] > llt_line[i-2]:
                signal.append(1)
            elif llt_line[i-1] < llt_line[i-2]:
                signal.append(-1)
            else:
                signal.append(signal[-1])

        signal.append(-1) # 最后平仓
        return signal