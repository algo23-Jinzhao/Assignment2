import pandas as pd
import baostock as bs
from tqdm import trange

def get_cap(code, year):
    
    # 2007年，取2006年四季度的流通股本，乘以2007年1月1日的昨收盘（后复权)
    if year == '2007':
        rs_profit = bs.query_profit_data(code=code, year=int(year), quarter=1) # 由于数据最早到2007年
    else:
        rs_profit = bs.query_profit_data(code=code, year=int(year)-1, quarter=4)
    df_profit = rs_profit.get_data()
    try:
        liqa_share = float(df_profit.loc[df_profit.index, 'liqaShare'].values[0])
    except:
        liqa_share = 0

    rs_price = bs.query_history_k_data_plus(code, "preclose", \
            start_date=str(int(year)-1)+'-12-01', end_date=str(int(year)-1)+'-12-31', frequency="d", adjustflag="1")
    price = float(rs_price.get_data().iloc[-1].values[0])
    
    return liqa_share * price

def func(arg1, arg2, arg3):
    cap_list.append([arg3, arg2[-6:], arg1(arg2, arg3)])
    
if __name__ == '__main__':
    df_components = pd.read_csv('沪深300成分股数据/components.csv')
    cap_list = []
    bs.login()
    for i in trange(len(df_components.columns)-1, desc='all years', position=1):
        date = df_components.columns[i]
        codes = df_components[date]
        year = date[:4]
        for j in trange(len(codes), desc=year, position=0):
            code = codes[j]
            func(get_cap, code, year)
    bs.logout()

    df_cap = pd.DataFrame(cap_list, columns=['year', 'code', 'cap'])

    def get_normalize(df):
        df['weight'] = df['cap'] / df['cap'].sum()
        return df[['year', 'code', 'weight']]

    df_weight = df_cap.groupby('year', group_keys=False).apply(get_normalize)
    df_weight.to_csv('沪深300成分股数据/weights.csv', index=False)



