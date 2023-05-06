from strategy.lltStrategy import LLTStrategy
from strategy.doubleMAStrategy import DoubleMAStrategy
from strategy.backTrendStrategy import BackTrendStrategy
from strategy.rumiStrategy import RUMIStrategy
from strategy.reverseStrategy import ReverseStrategy
from strategy.preTrendStrategy import PreTrendStrategy
from strategy.vnspStrategy import VNSPStrategy
from backTestEngine import sample_backtest, multi_backtest, portfolio_test, arg_analysis, multi_signal_test

def func1():
    # 单一策略的单股票择时回测
    task = (BackTrendStrategy, 20)
    stock_code = '000036'
    start_path = '沪深300成分股数据/data(adjust)/' + stock_code + '.csv'
    sample_backtest(task, start_path, stock_code, stop_win=0.1, stop_loss=-0.05)

def func2():
    # 单一策略的多参数多只股票择时回测
    task_list = [
        (BackTrendStrategy, 5),
        (BackTrendStrategy, 10),
        (BackTrendStrategy, 20),
        (BackTrendStrategy, 30),
        (BackTrendStrategy, 40),
        (BackTrendStrategy, 50),
        (BackTrendStrategy, 60),
        ] # 参数列表
    start_path = '沪深300成分股数据/data(adjust)'
    start_path_add = '沪深300成分股数据/weights.csv'
    end_path = 'stocks return/BackTrend'
    end_path_add = 'portfolio return/BackTrend.csv'
    start_date = '2007-04-05'
    end_date = '2022-12-31'
    multi_process = True
    multi_backtest(task_list, start_path, end_path, start_date, end_date, multi_process)
    portfolio_test(end_path, start_path_add, end_path_add, start_date, end_date)

def func3():
    # 单一策略的多参数多只股票择时回测
    task_list = [
        (RUMIStrategy, (5, 20)),
        (RUMIStrategy, (5, 30)),
        (RUMIStrategy, (5, 60)),
        (RUMIStrategy, (10, 20)),
        (RUMIStrategy, (10, 30)),
        (RUMIStrategy, (10, 60))
        ] # 参数列表
    start_path = '沪深300成分股数据/data(adjust)'
    start_path_add = '沪深300成分股数据/weights.csv'
    end_path = 'stocks return/RUMI'
    end_path_add = 'portfolio return/RUMI.csv'
    start_date = '2007-04-05'
    end_date = '2022-12-31'
    multi_process = True
    multi_backtest(task_list, start_path, end_path, start_date, end_date, multi_process)
    portfolio_test(end_path, start_path_add, end_path_add, start_date, end_date)

def func4():
    # 单一策略的多参数多只股票择时回测
    task_list = [
        (VNSPStrategy, (60, 20)),
        (VNSPStrategy, (60, 30)),
        (VNSPStrategy, (60, 60)),
        (VNSPStrategy, (40, 20)),
        (VNSPStrategy, (40, 30)),
        (VNSPStrategy, (40, 60))
        ] # 参数列表
    start_path = '沪深300成分股数据/data(adjust)'
    start_path_add = '沪深300成分股数据/weights.csv'
    end_path = 'stocks return/VNSP'
    end_path_add = 'portfolio return/VNSP.csv'
    start_date = '2007-04-05'
    end_date = '2022-12-31'
    multi_process = True
    multi_backtest(task_list, start_path, end_path, start_date, end_date, multi_process)
    portfolio_test(end_path, start_path_add, end_path_add, start_date, end_date)

def func5():
    # 采用多信号策略
    task_list = [
        (BackTrendStrategy, 40),
        (RUMIStrategy, (5, 60)),
        (VNSPStrategy, (40, 60))
        ]
    start_path = '沪深300成分股数据/data(adjust)'
    start_path_add = '沪深300成分股数据/weights.csv'
    end_path = 'stocks return/multisignal'
    end_path_add = 'portfolio return/multisignal.csv'
    start_date = '2007-04-05'
    end_date = '2022-12-31'
    multi_signal_test(task_list, start_path, end_path, start_date, end_date)
    portfolio_test(end_path, start_path_add, end_path_add, start_date, end_date)

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    #arg_analysis('portfolio return', 'figures')
    # 参数敏感性：BackTrend:[20,50], RUMI:[5,10]_[20,60], VNSP:[40,60]_[20,60]（这个因子对参数比较敏感，前面越小越好，后面越大越好）
    # 参数表现较好的：BackTrend:40, RUMI:5_60, VNSP:40_60
    #func5()
    arg_analysis('portfolio return', 'figures')

    '''
    task_list = [
        (LLTStrategy, 20), # llt斜率
        (DoubleMAStrategy, (5, 20)), # 简单双均线策略
        (ReverseStrategy, 60) # 反转策略
        # (PreTrendStrategy, 1), # 未来数据（当日收盘价，未来收盘价）（当日成交）
        ]  # 参数列表
    '''