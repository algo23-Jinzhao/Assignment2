import baostock as bs
import pandas as pd
from tqdm import trange
import os
import datetime

def date_deduct(in_date):
    dt = datetime.datetime.strptime(in_date, "%Y-%m-%d")
    out_date = (dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return out_date

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

def func(end_path, code, data_columns, start_date, end_date, adjustflag):
    
    rs = bs.query_history_k_data_plus(code, data_columns, start_date, end_date, 'd', adjustflag)
    df_result = rs.get_data()
    
    file_path = os.path.join(end_path, code[-6:] + '.csv')
    try:
        df_record = pd.read_csv(file_path)
        df_record = pd.concat([df_record, df_result])
        df_record.to_csv(file_path, index=False)
    except:
        # 覆盖原来的错误文件信息（文件夹内不存在指定的csv文件，csv文件内不存在指定格式的DataFrame）
        df_result.to_csv(file_path, index=False)
    

def get_data(end_path, data_columns, adjustflag):
    bs.login()
    for i in trange(len(df_components.columns)-1, desc='all years', position=1):
        start_date = df_components.columns[i]
        end_date = date_deduct(df_components.columns[i+1])
        codes = df_components[start_date]
        
        for j in trange(len(codes), desc=start_date, position=0):
            code = codes[j]
            func(end_path, code, data_columns, start_date, end_date, adjustflag)
    bs.logout()


data_columns = "date,code,open,high,low,close,volume,amount,turn,tradestatus,pctChg,isST"
df_components = pd.read_csv('components.csv')
'''
end_path = 'data'
# 清除文件夹内文件
if not os.path.exists(end_path):
    # 创建目标文件夹
    os.makedirs(end_path)
else:
    # 清除文件夹内文件
    clear_folder(end_path)
get_data(end_path, data_columns, '3')
'''
end_path_1 = 'data(adjust)'
# 清除文件夹内文件
if not os.path.exists(end_path_1):
    # 创建目标文件夹
    os.makedirs(end_path_1)
else:
    # 清除文件夹内文件
    clear_folder(end_path_1)
get_data(end_path_1, data_columns, '1')
