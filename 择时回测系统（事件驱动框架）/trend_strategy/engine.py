import pandas as pd
import os
import datetime
import chinese_calendar
from getPerformance import get_portfolio_indicators
from backTestEngine import BackTest
from multiprocessing import Pool, cpu_count
from tqdm import trange
import time


class DataEngine:
    def on_bar():


class TrendEngine:

    def send_order(self, price, volume):
        pass

    def get_value(postion):
        return net_value, unrealized_value

    # net_values->returns
    def get_returns(self, net_values, stock_values):
        strategy_returns = (net_values/net_values.shift()-1).fillna(0)
        benchmark_returns = (stock_values/stock_values.shift()-1).fillna(0)
        return strategy_returns, benchmark_returns
        

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                clear_folder(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

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

def func(arg1, arg2, arg3, arg4):
    arg1(arg2, arg3, arg4)
    
def multi_backtest(task_list, start_path, end_path, end_path_1, multi_process):
    # 清除文件夹内文件
    if not os.path.exists(end_path):
        # 创建目标文件夹
        os.makedirs(end_path)
    else:
        # 清除文件夹内文件
        clear_folder(end_path)

    # 清除文件夹内文件
    if not os.path.exists(end_path_1):
        # 创建目标文件夹
        os.makedirs(end_path_1)
    else:
        # 清除文件夹内文件
        clear_folder(end_path_1)

    files = os.listdir(start_path)

    if multi_process:
        start_time_1 = time.time()
        for i in trange(len(files), desc='all data', position=1):
            file = files[i]
            df_data = pd.read_csv(start_path + '/' + file, index_col=0)
            mybacktest = BackTest(df_data, end_path, end_path_1)
            # 对于每个CSV文件，创建一个新的多进程来处理它
            # 创建进程池
            pool = Pool(processes=cpu_count())
            for j in trange(len(task_list), desc='stock ' + file[:-4], position=0):
                task = task_list[j]
                pool.apply_async(func=func, args=(mybacktest.run_strategy, file[:-4], task[0], task[1],))
                time.sleep(0.01)
            # 关闭进程池
            pool.close()
            pool.join()
        end_time_1 = time.time()
        print('\n使用多进程 运行时间为{:.4}秒'.format(end_time_1-start_time_1))
    else:
        start_time_2 = time.time()
        for i in range(len(files)):
            file = files[i]
            df_data = pd.read_csv(start_path + '/' + file, index_col=0)

            mybacktest = BackTest(df_data, end_path)
            for j in range(len(task_list)):
                task = task_list[j]
                mybacktest.run_strategy(file[:-4], task[0], task[1])

        end_time_2 = time.time()
        print('\n不使用多进程 运行时间为{:.4}秒'.format(end_time_2-start_time_2))

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

def portfolio_backtest(start_path_1, start_path_2, end_path_2):
    date_index = get_tradeday('2012-04-09', '2019-12-31')

    files = os.listdir(start_path_1)
    df1 = pd.DataFrame(index=date_index)
    for file in files:
        df = pd.read_csv(start_path_1 + '/' + file, index_col=0)
        df.index = pd.to_datetime(df.index).values.astype('datetime64[D]')
        df.fillna(0, inplace=True)
        df1[file[:-4]] = df.sum(axis=1)

    files_1 = os.listdir(start_path_2)
    df3 = pd.DataFrame(index=df1.index)
    for file in files_1:
        df2 = pd.read_csv(start_path_2 + '/' + file)
        df2['date'] = pd.to_datetime(df2['date']).values.astype('datetime64[D]')
        df2.set_index('date', inplace=True)
        df4 = df3.copy()
        df4[file[:-4]] = df2['market_cap']
        df3 = df4.copy()
    series_total_size = df3.sum(axis=1)

    df_returns = pd.DataFrame(index=df1.index)
    for column in df1.columns:
        df_returns[column] = df1[column] / series_total_size
        get_valuation(column, df_returns[column])
    df_returns.fillna(0, inplace=True)
    df_returns.to_csv(end_path_2)