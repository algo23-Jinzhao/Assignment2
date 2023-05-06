import numpy as np

# 计算总收益率
def total_returns(returns):
    cum_returns = (1 + returns).cumprod()[-1] - 1
    return round(cum_returns, 4)

# 计算年化收益率
def annualized_returns(returns):
    total_return = total_returns(returns)
    if total_return >= -1:
        return round(np.power(1 + total_return, 252/len(returns.index))-1, 4)
    else:
        return -1
    
# 计算最大回撤率
def MDD(returns):
    cum_values = (1 + returns).cumprod()
    return max(1 - cum_values/cum_values.cummax()) 

def get_indicators(returns):
    return annualized_returns(returns), MDD(returns)

'''
def get_valuation(myStrategy_name, portfolio_returns):
    # 定义策略评价指标
    given_columns=['策略', '回测起始日期', '回测截止日期', '总收益率', '年化收益率', \
                        '最大回撤率', '最大回撤开始日期', '最大回撤结束日期', \
                            '总天数', '交易天数', '交易频率', '胜率', '盈亏比', '夏普比率']
    try:
        file_path = 'portfolio valuation.csv'
        df_result = pd.read_csv(file_path, dtype=str)
        df_result.columns = given_columns

        # 更新新的策略
        if myStrategy_name not in df_result['策略'].values:
            new_row = {'策略':myStrategy_name}
            for i in range(1, len(df_result.columns)):
                new_row[df_result.columns[i]] = get_portfolio_indicators(portfolio_returns)[i-1]
            df_result.loc[len(df_result)] = new_row

        # 修改原来策略的信息
        else:
            new_row = []
            for i in range(1, len(df_result.columns)):
                new_row.append(get_portfolio_indicators(portfolio_returns)[i-1])
            df_result.loc[df_result['策略'] == myStrategy_name, df_result.columns[1:]] = new_row
    except:

        # 覆盖原来的错误文件信息（文件夹内不存在指定的csv文件，csv文件内不存在指定格式的DataFrame）
        df_result = pd.DataFrame(columns=given_columns)
        new_row = {'策略':myStrategy_name}
        for i in range(1, len(df_result.columns)):
            new_row[df_result.columns[i]] = get_portfolio_indicators(portfolio_returns)[i-1]
        df_result.loc[len(df_result)] = new_row

    df_result.to_csv(file_path, index=False)

def max_drawdown(returns):
    cum_returns = (1 + returns).cumprod()

    max_drawdown = 0
    index_max = mdd_start = mdd_end = cum_returns.index[0]
    for i in cum_returns.index:
        if cum_returns.loc[i] > cum_returns.loc[index_max]:
            index_max = i
        else:
            drawdown = 1 - cum_returns.loc[i] / cum_returns.loc[index_max]
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                mdd_start = index_max
                mdd_end = i    

    return round(max_drawdown, 4), mdd_start, mdd_end

# 计算夏普比率
def sharpe_ratio(returns, risk_free_return):
    excess_returns = returns - (np.power(1 + risk_free_return, 1/365.25) - 1) # 日度无风险利率
    annualized_excess_returns = annualized_returns(excess_returns)
    annualized_volatility = np.std(returns) * np.sqrt(252)
    return round(annualized_excess_returns / annualized_volatility, 2)

# 计算年化超额收益率
def annualized_excess_returns(returns, benchmark_returns):
    return round(annualized_returns(returns) - annualized_returns(benchmark_returns), 4)

# 计算信息比率
def information_ratio(returns, benchmark_returns):
    active_volatility = np.std(returns - benchmark_returns) * np.sqrt(252) # 日波动率转化成年化波动
    return round(annualized_excess_returns(returns, benchmark_returns) / active_volatility, 2)

# 计算交易天数，开平仓次数，交易频率，胜率和盈亏比
def win_loss_ratio(returns):
    wins = len(returns[returns > 0])
    losses = len(returns[returns < 0])
    win_ratio = wins / (wins + losses)
    average_win = returns[returns > 0].mean()
    average_loss = returns[returns < 0].mean()
    return len(returns), wins+losses, round((wins+losses)/len(returns), 2), round(win_ratio, 4), round(abs(average_win / average_loss), 2)

# 计算年化主动投资收益率
def annualized_active_returns(returns, benchmark_returns):
    active_returns = returns - benchmark_returns
    return round(annualized_returns(active_returns), 4)

def get_indicators(returns, benchmark_returns):

    tr = total_returns(returns)
    ar = annualized_returns(returns)
    aer = annualized_excess_returns(returns, benchmark_returns)
    ir = information_ratio(returns, benchmark_returns)
    mdd, mdd_start_date, mdd_end_date = max_drawdown(returns)
    total_days, trading_days, trading_frequency, win_ratio, pnl = win_loss_ratio(returns)
    sharpe_r = sharpe_ratio(returns, risk_free_return=0.02)
    aar = annualized_active_returns(returns, benchmark_returns) # 为什么总是负的
    
    return str(returns.index[0])[:10], str(returns.index[-1])[:10], tr, ar, \
        mdd, str(mdd_start_date)[:10], str(mdd_end_date)[:10], \
        aer, ir, total_days, trading_days, trading_frequency, win_ratio, pnl, sharpe_r, aar

def get_portfolio_indicators(returns):
    tr = total_returns(returns)
    ar = annualized_returns(returns)
    mdd, mdd_start_date, mdd_end_date = max_drawdown(returns)
    total_days, trading_days, trading_frequency, win_ratio, pnl = win_loss_ratio(returns)
    sharpe_r = sharpe_ratio(returns, risk_free_return=0.02)
    return str(returns.index[0])[:10], str(returns.index[-1])[:10], tr, ar, \
        mdd, str(mdd_start_date)[:10], str(mdd_end_date)[:10], \
        total_days, trading_days, trading_frequency, win_ratio, pnl, sharpe_r

def get_portfolio_plot(names, returns, benchmark_returns):
    plt.figure(figsize=(40, 8))
    for name in names:
        values = (1 + returns[name]).cumprod()
        plt.plot(values.index, values, label=name)
    benchmark_values = (1+benchmark_returns).cumprod()
    plt.plot(benchmark_values.index, benchmark_values, label='CSI 300')
    plt.legend()
    plt.savefig('strategy net value.png')
    plt.show()
'''