import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.sans-serif"]=["SimHei"] # 设置字体
plt.rcParams["axes.unicode_minus"]=False # 该语句解决图像中的“-”负号的乱码问题

def get_value_plot(stock_values, net_values, unrealized_values):
    # 绘制净值曲线对比图
    benchmark_index = stock_values.index
    plt.figure(figsize=(40, 8))
    plt.plot(benchmark_index, stock_values, label='stock values')
    plt.plot(benchmark_index, net_values, color='red', label='net values')
    plt.plot(benchmark_index, unrealized_values, color='orange', label='unrealized values')
    plt.legend()
    plt.show()

def get_portfolio_value_plot(end_path, title, portfolio_returns, benchmark_value):
    dates = portfolio_returns.index
    plt.figure(figsize=(40, 8))
    plt.plot(dates, benchmark_value, label='CSI300')
    for column in portfolio_returns.columns:
        portfolio_return = portfolio_returns[column]
        portfolio_value = (1 + portfolio_return).cumprod()
        plt.plot(dates, portfolio_value, label=column)
    plt.title(title)
    plt.legend()
    plt.savefig(end_path + '/' + title + '_values.png')
    plt.show()

def get_indicators_plot(end_path, title, indic_dict):
    # 绘制参数敏感性分析图
    plt.figure(figsize=(40, 8))
    for arg in indic_dict:
        point_array = np.array(indic_dict[arg])
        plt.scatter(point_array[0], point_array[1], label=arg)
    plt.xlabel('年化收益率')
    plt.ylabel('最大回撤率')
    plt.title(title)
    plt.legend()
    plt.savefig(end_path + '/' + title + '_indicators.png')
    plt.show()