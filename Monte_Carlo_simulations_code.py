import pandas as pd
import numpy as np
from math import radians, sin, cos, asin, sqrt
import datetime

def haversine_dis(lon1, lat1, lon2, lat2):
    # 将十进制转为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    aa = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(aa))
    r = 6371  # 地球半径，千米
    return c * r


file_name = r'1.csv'
df1 = pd.read_csv(file_name)
file_name2 = r'1000.csv'
df2 = pd.read_csv(file_name2)
df2.rename(columns = {'name':'name1'}, inplace = True)
m = pd.concat([pd.concat([df1] * len(df2)).sort_index().reset_index(drop=True),
               pd.concat([df2] * len(df1)).reset_index(drop=True)], 1)
m['dis'] = m[['lon1', 'lat1', 'lon2', 'lat2']].apply(
    lambda x: haversine_dis(x['lon1'], x['lat1'], x['lon2'], x['lat2']), axis=1)

le=1000
gb=3

def x2p(x):
    if 1 > x:
        p = 0.6694
    elif 1 < x <= 3:
        p = 0.2231
    elif 3 < x <= 10:
        p = 0.0744
    elif 10 < x <= 20:
        p = 0.0248
    elif 20 < x <= 40:
        p = 0.0083
    elif 40 < x <= 60:
        p = 0.0000
    elif 60 < x :
        p = 0.000
    return p

b=0.0196
ca=0.0608

def gain_c(m):
    c = 0
    q = m['p']
    x = m['dis']
    if 1 > x:
        c = (0.6694 / q)  * x * (b * 0.1 + ca * 0.1)

    if 1 < x <= 3:
        c = (0.2231 / q)  * x * (b * 0.2667 + ca * 0.5333)

    if 3 < x <= 10:
        c = (0.0744 / q) * x * (b * 0.25 + ca * 0.75)

    if 10 < x <= 20:
        c = (0.0248 / q)  * x * (b * 0.20 + ca * 0.80)

    if 20 < x <= 40:
        c = (0.0083 / q) * x * (b * 0.1667 + ca * 0.8333)

    if 40 < x <= 60:
        c = (0.000 / q) * x * (b * 0.1429 + ca * 0.8571)

    if x > 60:
        c = (0.000 / q)  * x * (b * 0.1250 + ca * 0.8750)

    return c
def gain_p(x, m):
    
    temp = m[m['name1']==x]
    p = []
    for i in temp['dis']:
        p.append(x2p(i))
    return sum(p)



m['p'] = m['name1'].apply(lambda x:gain_p(x,m))
m['c'] = m.apply(gain_c, axis=1)

print(m)
print('总距离')
print(np.sum(m['dis']))

print('平均距离')
print(np.mean(m['dis']))

print('人均碳排放')
print(np.sum(m['c'])/le)

print('平均碳排放')
print(np.mean(m['c']))

print('总碳排放')
print(np.sum(m['c']))

print(file_name)
print(file_name2)


# 创建一个DataFrame
data = {'平均距离':[np.mean(m['dis'])], '人均碳排放':[np.sum(m['c'])/le], '汽车':[ca], '公交':[b], '公比':[gb], '总碳排放':[np.sum(m['c'])], '平均碳排放':[np.mean(m['c'])], '总距离':[np.sum(m['dis'])], '文件名':[file_name]}
df = pd.DataFrame(data)

res=file_name+'---'+file_name2
time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

# 将DataFrame写入Excel文件
df.to_excel( res +time+ '.xlsx', index=False)
