import pandas as pd
import os
from getPerformance import get_indicators, get_value_plot
import chinese_calendar
import datetime

def get_tradeday(start_str, end_str):
    start = datetime.datetime.strptime(start_str, '%Y-%m-%d') # 将字符串转换为datetime格式
    end = datetime.datetime.strptime(end_str, '%Y-%m-%d')
    # 获取指定范围内工作日列表
    lst = chinese_calendar.get_workdays(start,end)
    expt = []
    # 找出列表中的周六，周日，并添加到空列表
    for time in lst:
        if time.isoweekday() == 6 or time.isoweekday() == 7:
            expt.append(time)
    # 将周六周日排除出交易日列表
    for time in expt:
        lst.remove(time)
    date_list = [item.strftime('%Y-%m-%d') for item in lst] # 列表生成式，strftime为转换日期格式
    return date_list

class BacktestingEngine:
    def __init__(self, initial_data, end_path, portfolio_path) -> None:
        self.initial_data = initial_data
        self.end_path = end_path
        self.portfolio_path = portfolio_path
        
    def run_strategy(self, stock_code, class_name, parameters, portfolio=True, stop_win=0, stop_loss=0, value_plot=False):
        # 运行策略
        initial_data = self.initial_data
        myStrategy = class_name(initial_data)
        myStrategy_name = myStrategy.class_name_str()
        df_data = myStrategy.get_data()
        signals = myStrategy.get_signal(parameters)
        accurate_rate = myStrategy.get_accurate_rate(signals)
        stock_values, net_values, unrealized_values = myStrategy.get_trading(signals, stop_win, stop_loss)
        strategy_returns, benchmark_returns = myStrategy.get_returns(net_values, stock_values) # 这里有问题
        
        # 加入到投资组合中
        portfolio_returns = pd.DataFrame(index=get_tradeday('2012-01-01', '2019-12-31'))[60:] # calculate_days
        portfolio_returns[stock_code] = strategy_returns * df_data['market_cap'][60:] # calculate_days

        # 绘制净值曲线图
        # get_value_plot(value_plot, stock_values, net_values, unrealized_values, stock_code)
        
        # 定义文件名
        filename = myStrategy_name[:-8] + '.csv'

        # 定义策略评价指标
        given_columns=['stock_code', '判断准确率', '回测起始日期', '回测截止日期', '总收益率', '年化收益率', \
                            '最大回撤率', '最大回撤开始日期', '最大回撤结束日期', '年化超额收益率', '信息比率', \
                                '总天数', '交易天数', '交易频率', '胜率', '盈亏比', '夏普比率', '年化主动投资收益率']

        try:
            file_path = os.path.join(self.end_path, filename)
            df_result = pd.read_csv(file_path, dtype=str)
            df_result.columns = given_columns

            # 更新新的股票
            if stock_code not in df_result['stock_code'].values:
                new_row = {'stock_code':stock_code, '判断准确率':accurate_rate}
                for i in range(2, len(df_result.columns)):
                    new_row[df_result.columns[i]] = get_indicators(strategy_returns, benchmark_returns)[i-2]
                df_result.loc[len(df_result)] = new_row

            # 修改原来股票的信息
            else:
                new_row = [round(accurate_rate, 4)]
                for i in range(2, len(df_result.columns)):
                    new_row.append(get_indicators(strategy_returns, benchmark_returns)[i-2])
                df_result.loc[df_result['stock_code'] == stock_code, df_result.columns[1:]] = new_row
        except:

            # 覆盖原来的错误文件信息（文件夹内不存在指定的csv文件，csv文件内不存在指定格式的DataFrame）
            df_result = pd.DataFrame(columns=given_columns)
            new_row = {'stock_code':stock_code, '判断准确率':accurate_rate}
            for i in range(2, len(df_result.columns)):
                new_row[df_result.columns[i]] = get_indicators(strategy_returns, benchmark_returns)[i-2]
            df_result.loc[len(df_result)] = new_row

        df_result.to_csv(self.end_path + '/' + filename, index=False)

        if portfolio == True:
            try:
                df_portfolio = pd.read_csv(self.portfolio_path + '/' + myStrategy_name[:-8] + '.csv', index_col=0)
                if df_portfolio.empty:
                    df_portfolio = portfolio_returns
                else:
                    df_portfolio = df_portfolio.join(portfolio_returns) 
                df_portfolio.to_csv(self.portfolio_path + '/' + myStrategy_name[:-8] + '.csv')
            except:
                portfolio_returns.to_csv(self.portfolio_path + '/' + myStrategy_name[:-8] + '.csv')

    