import baostock as bs
import pandas as pd

def get_components(dates):
    df_components = pd.DataFrame()
    for date in dates:
        print(date)
        # 登陆系统
        bs.login()
        
        # 获取沪深300成分股
        rs = bs.query_hs300_stocks(date)
        # 打印结果集
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            hs300_stocks.append(rs.get_row_data()[1])

        # 登出系统
        bs.logout()
        df_components[date] = hs300_stocks
    return df_components
dates = [str(i)+'-01-01' for i in range(2007, 2024)]
df_components = get_components(dates)
df_components.to_csv('components.csv', index=False)