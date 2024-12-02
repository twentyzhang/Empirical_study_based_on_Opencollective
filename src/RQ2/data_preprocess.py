import pandas as pd
import os
from datetime import datetime

def findFile(files,name):
    for file in files:
        if file[0:len(file) - 4]==name:
            return file
    return ''

data=pd.read_csv('./data.csv')
files=os.listdir('./data/member/member')

for row in range(len(data)):
    name=data.loc[row,'Slug']
    file=findFile(files,name)
    if(file==''):
        data.drop(data.index[row])
        continue

    member=pd.read_csv('./data/member/member/'+file)
    total=0
    for i in range(len(member)):
        amount=member.loc[i,'Donations']
        money=member.loc[i,'Currency']
        if money == 'EUR':
            amount = amount * 1.1
        elif money == 'USD':
            amount = amount
        elif money == 'GBP':
            amount = amount * 1.3
        elif money == 'BRL':
            amount = amount * 0.18
        elif money == 'JPY':
            amount = amount / 149.0
        elif money == 'CHF':
            amount = amount * 1.17
        elif money == 'DKK':
            amount = amount * 0.15
        elif money == 'CAD':
            amount = amount * 0.73
        elif money == 'PLN':
            amount = amount * 0.25
        elif money == 'MYR':
            amount = amount * 0.23
        elif money == 'MXN':
            amount = amount * 0.05
        elif money == 'TRY':
            amount = amount * 0.03
        elif money == 'SGD':
            amount = amount * 0.77
        elif money == 'INR':
            amount = amount * 0.01
        elif money == 'CNY':
            amount = amount * 0.14
        elif money=='BGN':
            amount=amount*0.53
        elif money=='UAH':
            amount=amount*0.024
        elif money=='HKD':
            amount=amount*0.13
        elif money=='SEK':
            amount=amount*0.09
        elif money=='NZD':
            amount=amount*0.58
        elif money=='KRW':
            amount=amount*0.00071
        else:
            print(money)
        total+=amount
    data.loc[row,'Donations']=int(total)
    if total==0:
        data.loc[row,'isDonated']=0
    else:
        data.loc[row,'isDonated']=1
    create_time=data.loc[row,'create_time']
    # 解析时间字符串
    start_date = datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    # 目标日期
    end_date = datetime(2024, 11, 1)
    # 计算差异的年和月
    months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    data.loc[row,'existTime']=months_diff

data.to_csv('data.csv')

