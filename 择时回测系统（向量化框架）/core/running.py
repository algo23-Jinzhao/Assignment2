from strategy.lltStrategy import LLTStrategy
from strategy.doubleMAStrategy import DoubleMAStrategy
from strategy.backTrendStrategy import BackTrendStrategy
from strategy.rumiStrategy import RUMIStrategy
from strategy.reverseStrategy import ReverseStrategy
from strategy.preTrendStrategy import PreTrendStrategy
from strategy.vnspStrategy import VNSPStrategy
from backTester import multi_backtest, portfolio_backtest
from strategyEvaluation import startEvaluation

if __name__ == '__main__':

    task_list = [
        (VNSPStrategy, (60, 20, 5)),  # vnsp因子
        (LLTStrategy, 20), # llt斜率
        (DoubleMAStrategy, (5, 20)), # 简单双均线策略
        (RUMIStrategy, (5, 20, 10)), # rumi策略
        (BackTrendStrategy, 20), # 动量策略
        (ReverseStrategy, 60) # 反转策略
        # (PreTrendStrategy, 1), # 未来数据（当日收盘价，未来收盘价）（当日成交）
        ]  # 参数列表
    start_path = 'train set'
    end_path = 'result'
    end_path_1 = 'stock returns'
    multi_process = True
    
    start_path_1 = 'stock returns'
    start_path_2 = 'train set'
    end_path_2 = 'portfolio result.csv'
    
    #multi_backtest(task_list, start_path, end_path, end_path_1, multi_process)
    portfolio_backtest(start_path_1, start_path_2, end_path_2)

    start_path_3 = 'result'
    end_path_3 = 'figures'
    end_path_4 = 'figures(portfolio)'
    strategy_list = ['VNSP', 'LLT', 'DoubleMA', 'Rumi', 'BackTrend', 'Reverse']
    portfolio = False
    startEvaluation(start_path_3, end_path_3, strategy_list, portfolio, end_path_4)
    