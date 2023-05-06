import akshare as ak

index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20070104", end_date="20221230")
index_zh_a_hist_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'swing', 'pctChg', 'pctChgAmount', 'turn']
index_zh_a_hist_df.to_csv('沪深300成分股数据/沪深300.csv', index=False)