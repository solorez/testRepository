'''
缠论-pandas版
'''
from pandas import DataFrame
import numpy as np
from datetime import datetime
import tushare as tu
import pandas as pd

stock_code = '601318'
start_date = '2016-02-05'
end_date = '2017-02-07'
initial_trend = "down"

# bars = DataFrame(data=[],
#                  index=[datetime.now()],
#                  columns=['open1','close','high','low','volume','money'])
bars = tu.get_k_data(code=stock_code,
                     start=start_date,
                     end=end_date,
                     ktype='D',  # D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
                     autype='qfq'
                     ).sort_index(ascending=True)
bars = bars.dropna(how='any')
bars = bars.reset_index(drop=True)
# bars['dingfenxing'] = False

def biaoDingDiFenXing():
    '''
    初次标记顶底，增加‘fenxing’列:顶分型：1、底分型：-1、非顶非底：0
    :return: DataFrame 
    '''
    bars['fenxing'] = 0
    i = 1
    while i < len(bars)-1:
        if bars.loc[i-1,'high'] < bars.loc[i,'high'] and bars.loc[i,'high'] > bars.loc[i+1,'high']\
                and bars.loc[i-1,'low'] < bars.loc[i,'low'] and bars.loc[i,'low'] > bars.loc[i+1,'low']:
            bars.loc[i,'fenxing'] = 1
        elif bars.loc[i-1,'low'] > bars.loc[i,'low'] and bars.loc[i,'low'] < bars.loc[i+1,'low']\
                and bars.loc[i-1,'high'] > bars.loc[i,'high'] and bars.loc[i,'high'] < bars.loc[i+1,'high']:
            bars.loc[i,'fenxing'] = -1
        i = i+1
    with pd.ExcelWriter('/home/fubo/zenTheory.xls') as writer:
        bars.to_excel(writer)
    return bars
biaoDingDiFenXing()
def zhaoChuShiFangXiang():
    '''
    从最初k线找到起始方向
    :return: 
    '''

def heBingKxian():
    '''
    合并具有包含关系的K线。
    包含量['baoHanLiang']：
        0：合并0根k线
        i：合并i根k线
    :return:    
    '''
    pass

def biaoDingDi():
    '''
    标记真正的顶和底
    :return: 
    '''



