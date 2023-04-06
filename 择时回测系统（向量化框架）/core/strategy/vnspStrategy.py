from strategyTemplate import BasicStrategy
import numpy as np

def LLT(data, d):
    llt = [(data[0]+data[1])/2, (data[0]+data[1])/2]
    alpha = 2/(d+1)
    for i in range(2, len(data)):
        llt.append((alpha-alpha**2/4)*data[i] + alpha**2/2*data[i-1] - (alpha-3*alpha**2/4)*data[i-2] \
            + 2*(1-alpha)*llt[i-1] - (1-alpha)**2*llt[i-2])
    return llt

def get_factors(df, n):
    for i in range(n, len(df.index)-1):
        # 得到i-1到i-n这段的数据, 换手率计算权重
        initial_array = 1 - df.loc[df.index[i-n]:df.index[i-1], 'average'] / df.loc[df.index[i], 'average']
        array_1 = df.loc[df.index[i-n]:df.index[i-1], 'turnover_ratio']
        array_2 = (1-array_1).iloc[::-1].shift().fillna(1).cumprod().iloc[::-1]
        w_array = array_1 * array_2
        w_array_pct = w_array / w_array.sum()
        gain_loss_array = initial_array * w_array_pct
        gain = 0
        loss = 0
        for j in gain_loss_array:
            if j > 0 :
                gain += j
            elif j < 0:
                loss += j
        df.loc[df.index[i+1], 'gain'] = gain
        df.loc[df.index[i+1], 'loss'] = loss
    return df.fillna(0)

class VNSPStrategy(BasicStrategy):
    def __init__(self, initial_data) -> None:
        super(VNSPStrategy, self).__init__(initial_data)
        
    def get_signal(self, parameters:list) -> list:
        df2 = self.df2
        n, d, d_vnsp = parameters
        df_factors = get_factors(df2, n) 
        df_factors['gain_llt'] = LLT(df_factors['gain'], d)
        df_factors['loss_llt'] = LLT(df_factors['loss'], d)
        df_factors['vnsp_llt'] = LLT(df_factors['gain_llt'] + np.square(df_factors['loss_llt']), d_vnsp)
        llt_window = max(d + d_vnsp, n)
        series_factors = df_factors['vnsp_llt']

        signal = [0]*llt_window
        for i in range(llt_window, len(df2.index)-1):
            if series_factors[i] > series_factors[i-1]:
                signal.append(1)
            elif series_factors[i] < series_factors[i-1]:
                signal.append(-1)
            else:
                signal.append(signal[-1])
        signal.append(-1) # 最后平仓
        return signal