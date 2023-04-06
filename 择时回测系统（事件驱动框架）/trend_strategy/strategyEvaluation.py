import os
import pandas as pd
import matplotlib.pyplot as plt
from getPerformance import get_portfolio_plot

plt.rcParams["font.sans-serif"]=["SimHei"] # 设置字体
plt.rcParams["axes.unicode_minus"]=False # 该语句解决图像中的“-”负号的乱码问题

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

def individual_stocks(start_path, end_path, strategy_list, indicator_list = \
        ['判断准确率', '年化收益率', '最大回撤率', '年化超额收益率', '信息比率', \
         '交易频率', '胜率', '盈亏比', '夏普比率', '年化主动投资收益率']):
    # 画个策略对比图
    if not os.path.exists(end_path):
        # 创建目标文件夹
        os.makedirs(end_path)
    else:
        # 清除文件夹内文件
        clear_folder(end_path)
    
    for indicator in indicator_list:
        plt.figure(figsize=(40, 8))
        for i in strategy_list:
            df = pd.read_csv(start_path + '/' + i + '.csv', dtype={'stock_code':object})
            plt.plot(df['stock_code'], df[indicator], label=i)
        plt.xticks(rotation=30)
        plt.title(indicator)
        plt.legend()
        plt.savefig(end_path + '/' + indicator + '.png')
        plt.show()

def portfolio_stocks(end_path):
    # 绘制不同策略的净值曲线
    df_returns = pd.read_csv('portfolio result.csv', index_col=0)
    df_returns.index = pd.to_datetime(df_returns.index).values.astype('datetime64[D]')
    df_csi = pd.read_csv('沪深300.csv', index_col=0)
    df_csi.index = pd.to_datetime(df_csi.index).values.astype('datetime64[D]')
    df_benchmark = df_csi.loc[df_returns.index[0]:df_returns.index[-1], '收盘']
    df_benchmark_returns = (df_benchmark/df_benchmark.shift()-1).fillna(0)
    get_portfolio_plot(df_returns.columns, df_returns, df_benchmark_returns)

    # 画个策略对比图
    if not os.path.exists(end_path):
        # 创建目标文件夹
        os.makedirs(end_path)
    else:
        # 清除文件夹内文件
        clear_folder(end_path)

    file_path = 'portfolio valuation.csv'
    df = pd.read_csv(file_path)

    s = df['策略']
    x1 = df['年化收益率'] 
    x2 = df['最大回撤率']
    x3 = df['夏普比率']

    #绘制第一个Y轴
    fig = plt.figure(figsize=(40,8), dpi=80)
    ax = fig.add_subplot(111)
    lin1 = ax.plot(s, x1, color='red', label='年化收益率')
    lin2 = ax.plot(s, x2, color='green', label='最大回撤率')
    
    #绘制另一Y轴    
    ax1 = ax.twinx()
    lin3 = ax1.plot(s, x3, color='blue', label='夏普比率')
    
    #合并图例
    lins = lin1 + lin2 + lin3
    labs = [l.get_label() for l in lins]
    ax.legend(lins, labs, loc="upper left", fontsize=15)
    ax.set_ylabel('年化收益率（最大回撤率）')
    ax1.set_ylabel('夏普比率')
    plt.savefig(end_path + '/1.png')
    plt.show()

    # 画出胜率和盈亏比的散点图
    fig = plt.figure(figsize=(40,8), dpi=80)
    x = df['胜率']
    y = df['盈亏比'] 
    sc = plt.scatter(x, y, c=df['交易频率'], cmap='YlGnBu')  
    plt.colorbar(sc)  
    plt.xlabel('胜率')
    plt.ylabel('盈亏比')
    plt.savefig(end_path + '/2.png')
    plt.show()

def startEvaluation(start_path, end_path_individual, strategy_list, portfolio, end_path_portfolio):
    if portfolio:
        portfolio_stocks(end_path_portfolio)
    else:
        individual_stocks(start_path, end_path_individual, strategy_list)
