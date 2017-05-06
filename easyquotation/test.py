
from chan_lun_util import *
# from k_line_dto import *
import matplotlib as mat
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import time
import tushare as tu
import pandas as pd
from pandas import DataFrame

stock_code = '601318'
start_date = '2016-02-05'
end_date = '2017-02-07'
initial_trend = "down"

'''
以下代码拷贝自https://www.joinquant.com/post/1756
'''
# quotes = get_price(stock_code, start_date, end_date, frequency='daily', skip_paused=False, fq='pre')
quotes = tu.get_hist_data(stock_code,
                          start=start_date,
                          end=end_date,
                          ktype='D',   # D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
                          ).sort_index(ascending = True)

quotes = tu.get_k_data(code=stock_code,
                       start=start_date,
                       end=end_date,
                       ktype='D',   # D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
                       autype='qfq'
                       ).sort_index(ascending = True)
#task1 quotes.index 数据类型 object》》》datetime64[ns]
#quotes['index2'] = quotes.index.map(lambda x:datetime.strptime(x,'%Y-%m-%d'))
quotes.index = pd.to_datetime(quotes['date']) # convert quotes.index from object to datetime64
# task2 列切片与jointquant完全相同
quotes[quotes['volume']==0]=np.nan
quotes= quotes.dropna()
# 删除不需要的数据
# quotes = quotes.drop(['price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20'],axis=1)
#调整列顺序为jointquant顺序
quotes = quotes.ix[:,['open','close','high','low','volume']]
quotes['money'] = quotes['open'] * quotes['volume']
# # 本地保存
# with pd.ExcelWriter('/home/fubo/huizhifenbi.xls') as writer:
#     quotes.to_excel(writer)

Close=quotes['close']
Open=quotes['open']
High=quotes['high']
Low=quotes['low']
T0 = quotes.index.values



# 处理分笔结果，组织成实际上图的点
k_line_list = []
date_list = quotes.index.tolist()
data_per_day = quotes.values.tolist()
x_date_list = quotes.index.values.tolist()

for index in range(len(date_list)):
    date_time = date_list[index]
    open_price = data_per_day[index][0]
    close_price = data_per_day[index][1]
    high_price = data_per_day[index][2]
    low_price = data_per_day[index][3]
    k_line_dto = KLineDTO(date_time,
                              date_time,
                              date_time,
                              open_price, high_price, low_price, close_price)
    k_line_list.append(k_line_dto)

#  1.K线合并，寻找顶底分型
merge_line_list = find_peak_and_bottom(k_line_list, initial_trend)
#  输出检查  indentical with joinQuant
'''
for m_line_dto in merge_line_list:
    print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + " -- " +
          m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "**" +
          m_line_dto.is_peak + "**" + m_line_dto.is_bottom + "**" +
          str(m_line_dto.stick_num))
'''