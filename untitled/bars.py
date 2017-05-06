from chan_lun_util import *
import numpy as np
import time
import tushare as tu
import pandas as pd

stock_code = '601318'
start_date = '2016-02-05'
end_date = '2017-02-07'
initial_trend = "down" # down

quotes = tu.get_k_data(code=stock_code,
                       start=start_date,
                       end=end_date,
                       ktype='D',  # D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
                       autype='qfq'
                       ).sort_index(ascending=True)
# task1 quotes.index 数据类型 object》》》datetime64[ns]
quotes.index = pd.to_datetime(quotes['date'])  # convert quotes.index from object to datetime64
# task2 列切片与jointquant完全相同
quotes[quotes['volume'] == 0] = np.nan
quotes = quotes.dropna()
# 删除不需要的数据

# 调整列顺序为jointquant顺序
quotes = quotes.ix[:, ['open', 'close', 'high', 'low', 'volume']]
quotes['money'] = quotes['open'] * quotes['volume']

# 生成eChart可识别的bars(datas)-开始
chartQuotes = quotes.ix[:, ['open', 'close', 'low', 'high']]  # 调整列顺序 ,'volume'
bars = []
bars = chartQuotes.to_csv(None, header=False, index=False).split('\n')  # 转化成列表
pre_datas = ''
for bar in bars:
    pre_datas = pre_datas + ('[%s],' % bar)  # '[%s]' %
datas = ('[%s]' % pre_datas[:-4])
dates = chartQuotes.index
pre_dates = ''
for date in dates:
    pre_dates = pre_dates + ("'%s'," % date.strftime('%Y/%m/%d'))
dates = ('[%s]' % pre_dates[:-1])
# 生成eChart可识别的bars(datas)--结束

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

# 1.K线合并，寻找顶底分型
merge_line_list = find_peak_and_bottom(k_line_list, initial_trend)
#  输出检查  indentical with joinQuant
# for m_line_dto in merge_line_list:
#     print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + " -- " +
#           m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "**" +
#           m_line_dto.is_peak + "**" + m_line_dto.is_bottom + "**" +
#           str(m_line_dto.stick_num))

#  2.分笔
fenbi_result, final_result_array, fenbi_seq_list = fen_bi(merge_line_list)
# print(fenbi_seq_list) # identical with joinQuant
print('fenbi_result:', fenbi_result)
print("final_result_array:", len(final_result_array), final_result_array)
print('fenbi_seq_list:', len(fenbi_seq_list), fenbi_seq_list)
#  3.得到分笔结果，计算坐标显示
x_fenbi_seq = []
y_fenbi_seq = []
for i in range(len(final_result_array)):
    if final_result_array[i]:
        m_line_dto = merge_line_list[fenbi_seq_list[i]]
        if m_line_dto.is_peak == 'Y':
            peak_time = None
            for k_line_dto in m_line_dto.member_list[::-1]:
                if k_line_dto.high == m_line_dto.high:
                    # get_price返回的日期，默认时间是08:00:00
                    peak_time = k_line_dto.begin_time.strftime('%Y-%m-%d') + ' 08:00:00'
                    break
            x_fenbi_seq.append(x_date_list.index(
                int(time.mktime(datetime.strptime(peak_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000000000)))
            y_fenbi_seq.append(round(m_line_dto.high, 2))
        if m_line_dto.is_bottom == 'Y':
            bottom_time = None
            for k_line_dto in m_line_dto.member_list[::-1]:
                if k_line_dto.low == m_line_dto.low:
                    # get_price返回的日期，默认时间是08:00:00
                    bottom_time = k_line_dto.begin_time.strftime('%Y-%m-%d') + ' 08:00:00'
                    break
            x_fenbi_seq.append(x_date_list.index(
                int(time.mktime(datetime.strptime(bottom_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000000000)))
            y_fenbi_seq.append(round(m_line_dto.low, 2))
fenbi = ''
for i in range(len(x_fenbi_seq) - 1):
    fenbi = fenbi + '[{xAxis:%s,yAxis:%s},{xAxis:%s,yAxis:%s}],' % (
        x_fenbi_seq[i], y_fenbi_seq[i], x_fenbi_seq[i + 1], y_fenbi_seq[i + 1])
fenbi = '[%s]' % (fenbi[:-1])
print(fenbi)
