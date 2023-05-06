import pandas as pd
import os
from multiprocessing import Pool, cpu_count
from tqdm import trange
import time
import csv
import chinese_calendar
import datetime
import numpy as np

from getPerformance import get_indicators
from getPlot import get_value_plot, get_portfolio_value_plot, get_indicators_plot

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

class BackTest:
    def __init__(self, initial_data, stock_code) -> None:
        self.initial_data = initial_data
        self.stock_code = stock_code

    def run_strategy(self, class_name, parameters, end_path=None, start_date=None, end_date=None, stop_win=0, stop_loss=0, value_plot=False):
        # 运行策略
        myStrategy = class_name(self.initial_data)
        # strategy_name = myStrategy.class_name_str()
        # 从原始数据中获取所需数据
        myStrategy.clear_data()
        # 得到信号
        signals = myStrategy.get_signal(parameters)
        # 得到买卖结果
        stock_values, net_values, unrealized_values = myStrategy.get_trading(signals, stop_win, stop_loss)
        # 绘制净值曲线
        if value_plot == True:
            get_value_plot(stock_values, net_values, unrealized_values)
        else: 
            
            strategy_returns = (net_values/net_values.shift()-1).fillna(0)

            # 转化成列表
            trade_days = get_tradeday(start_date, end_date)
            returns_list = [self.stock_code]
            for i in trade_days:
                if i in strategy_returns.index:
                    returns_list.append(strategy_returns.loc[i])
                else:
                    returns_list.append(0)

            # 得到文件名（用参数名代替）
            if type(parameters) == int:
                parameters_str = str(parameters)
            else:
                parameters_str = "_".join(str(i) for i in parameters)     

            file_path = end_path + '/' + parameters_str + '.csv' # 回测结果（stocks return）存放的位置
            with open(file_path, "a", newline='') as f: 
                writer = csv.writer(f)
                writer.writerow(returns_list)

    def run_multi_signal_strategy(self, task_list, end_path=None, start_date=None, end_date=None, stop_win=0, stop_loss=0, value_plot=False):
        try:
            signal_list = []
                
            for task in task_list:
                class_name = task[0]
                parameters = task[1]
                # 运行策略
                myStrategy = class_name(self.initial_data)
                # strategy_name = myStrategy.class_name_str()
                # 从原始数据中获取所需数据
                myStrategy.clear_data()
                # 得到信号
                signal = myStrategy.get_signal(parameters)
                signal_list.append(signal)

            signal_array = np.array(signal_list)
            for way in ['intersection', 'add']:
                if way == 'intersection':
                    # intersection
                    signals = []
                    for i in range(len(signal_array[0])):
                        if (signal_array[:, i] == 1).all():
                            signals.append(1)
                        elif (signal_array[:, i] == -1).all():
                            signals.append(-1)
                        else:
                            signals.append(0)
                elif way == 'add':
                    # add
                    signals = []
                    for i in range(len(signal_array[0])):
                        if signal_array[:, i].sum() > 0:
                            signals.append(1)
                        elif signal_array[:, i].sum() < 0:
                            signals.append(-1)
                        else:
                            signals.append(0)

                # 得到买卖结果
                stock_values, net_values, unrealized_values = myStrategy.get_trading(signals, stop_win, stop_loss)
                # 绘制净值曲线
                if value_plot == True:
                    get_value_plot(stock_values, net_values, unrealized_values)
                else: 
                    
                    strategy_returns = (net_values/net_values.shift()-1).fillna(0)

                    # 转化成列表
                    trade_days = get_tradeday(start_date, end_date)
                    returns_list = [self.stock_code]
                    for i in trade_days:
                        if i in strategy_returns.index:
                            returns_list.append(strategy_returns.loc[i])
                        else:
                            returns_list.append(0)  

                    file_path = end_path + '/' + way + '.csv' # 回测结果（stocks return）存放的位置
                    with open(file_path, "a", newline='') as f: 
                        writer = csv.writer(f)
                        writer.writerow(returns_list)
        except:
            pass

def sample_backtest(task, start_path, stock_code, stop_win, stop_loss, value_plot=True):
    df_data = pd.read_csv(start_path, index_col=0)
    mybacktest = BackTest(df_data, stock_code)
    mybacktest.run_strategy(task[0], task[1], stop_win=stop_win, stop_loss=stop_loss, value_plot=value_plot)

def func(arg1, arg2, arg3, arg4, arg5, arg6):
    arg1(arg2, arg3, arg4, arg5, arg6)
    
def multi_backtest(task_list, start_path, end_path, start_date, end_date, multi_process):

    files = os.listdir(start_path)
    if not os.path.exists(end_path):
        os.makedirs(end_path)
    else:
        clear_folder(end_path)

    if multi_process:
        start_time_1 = time.time()
        for i in trange(len(files), desc='all data', position=1):
            file = files[i]
            stock_code = file[:-4]
            df_data = pd.read_csv(start_path + '/' + file, index_col=0)
            mybacktest = BackTest(df_data, stock_code)
            # 对于每个CSV文件，创建一个新的多进程来处理它
            # 创建进程池
            pool = Pool(processes=cpu_count())
            for j in trange(len(task_list), desc='stock ' + file[:-4], position=0):
                task = task_list[j]
                pool.apply_async(func=func, args=(mybacktest.run_strategy, task[0], task[1], end_path, start_date, end_date))
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

            mybacktest = BackTest(df_data)
            for j in range(len(task_list)):
                task = task_list[j]
                mybacktest.run_strategy(task[0], task[1], end_path, start_date, end_date)

        end_time_2 = time.time()
        print('\n不使用多进程 运行时间为{:.4}秒'.format(end_time_2-start_time_2))


def portfolio_test(start_path, star_path_add, end_path, start_date, end_date):
    trade_days = get_tradeday(start_date, end_date)
    files = os.listdir(start_path)
    folder = end_path.split('/')[0]

    # 创建目标文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 得到组合收益率
    portfolio_returns = pd.DataFrame()
    for file in files:
        returns_dict = {}
        with open(start_path + '/' + file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                returns_dict[row[0]] = row[1:]

        # 得到每个参数对应的returns
        df_returns = pd.DataFrame(returns_dict, index=trade_days, dtype=float)
        # 得到每只股票每天的权重
        df_weights = pd.read_csv(star_path_add, dtype={'year':str, 'code':str})

        ret_list = []
        for date in df_returns.index:
            print(date)
            codes = df_weights[df_weights['year'] == date[:4]] 
            ret = 0
            for i in codes.index:
                try:
                    code = codes.loc[i, 'code']
                    weight = codes.loc[i, 'weight']
                    ret += (df_returns.loc[date, code] * weight)
                except:
                    pass
            ret_list.append(ret)
        ret_series = pd.Series(ret_list, index=df_returns.index)
        portfolio_returns[file[:-4]] = ret_series
    portfolio_returns.to_csv(end_path)

def arg_analysis(start_path, end_path):
    if not os.path.exists(end_path):
        os.makedirs(end_path)
    else:
        clear_folder(end_path)
    files = os.listdir(start_path)
    for file in files:
        file_path = start_path + '/' + file
        df_returns = pd.read_csv(file_path, index_col=0)
        df_returns.index = pd.to_datetime(df_returns.index).values.astype('datetime64[D]')

        # 引入基准指数
        df_benchmark = pd.read_csv('沪深300成分股数据/沪深300.csv', index_col=0)
        df_benchmark.index = pd.to_datetime(df_benchmark.index).values.astype('datetime64[D]')
        benchmark_value = df_benchmark.loc[df_returns.index, 'close']/df_benchmark.loc[df_returns.index, 'close'].iloc[0]
        #benchmark_returns = (benchmark_value/benchmark_value.shift()-1).fillna(0)
        get_portfolio_value_plot(end_path, file[:-4], df_returns, benchmark_value)

        indic_dict = {}
        for arg in df_returns.columns:
            returns = df_returns[arg]
            indic_dict[arg] = list(get_indicators(returns))
        get_indicators_plot(end_path, file[:-4], indic_dict)

def multi_signal_test(task_list, start_path, end_path, start_date, end_date):
    files = os.listdir(start_path)
    if not os.path.exists(end_path):
        os.makedirs(end_path)
    else:
        clear_folder(end_path)

    for i in trange(len(files), desc='all data'):
        file = files[i]
        stock_code = file[:-4]
        df_data = pd.read_csv(start_path + '/' + file, index_col=0)
        mybacktest = BackTest(df_data, stock_code)
        mybacktest.run_multi_signal_strategy(task_list, end_path, start_date, end_date)
    