import os
import pandas as pd

from strategy.lltStrategy import LLTStrategy
from strategy.doubleMAStrategy import DoubleMAStrategy
from strategy.backTrendStrategy import BackTrendStrategy
from strategy.rumiStrategy import RUMIStrategy
from strategy.reverseStrategy import ReverseStrategy
from strategy.preTrendStrategy import PreTrendStrategy
from strategy.vnspStrategy import VNSPStrategy

from getBackTest import BackTest
from multiprocessing import Pool, cpu_count
from tqdm import trange
import time

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

def func(arg1, arg2, arg3, arg4):
    arg1(arg2, arg3, arg4)
    
def main(task_list, start_path, end_path, end_path_1, multi_process):
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
    start_path = 'data'
    end_path = 'result'
    end_path_1 = 'portfolio'
    multi_process = True
    main(task_list, start_path, end_path, end_path_1, multi_process)

    