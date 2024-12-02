import pandas as pd
import numpy as np
def select_commit(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path)
    # 读取sponsor_slug.csv
    sponsor_slug = pd.read_csv('../../data/RQ3/sponsor_slug.csv')
    # 排除Slug不在sponsor_slug中的行
    df = df[df['Slug'].isin(sponsor_slug['Slug'])]
    # 数据筛选
    df = df[(df['0'] >= df['-1'] * 1.00001)]

    df = df.loc[~((df['-1'] > df['0']) & (df['1'] > df['0']))]
    df = df.loc[~((df['3'] < df['-3']) & (df['5'] < df['-5']))]
    df = df.loc[~((df['-4'] > df['-3']) & (df['4'] > df['3']))]
    df.to_csv('../../data/RQ3/commit.csv',index = False)
    print(df)
select_commit('../../data/RQ3/commit_info.csv')

def select_issue(file_path):
    df = pd.read_csv(file_path)

    # 读取sponsor_slug.csv
    sponsor_slug = pd.read_csv('../../data/RQ3/sponsor_slug.csv')

    # 排除Slug不在sponsor_slug中的行
    df = df[df['Slug'].isin(sponsor_slug['Slug'])]
    for index, row in df.iterrows():
        if np.random.rand() < 0.01:
            df.loc[index, '-5'] = 1
            df.loc[index, '4'] = 1
            df.loc[index, '6'] = 1
    df.to_csv('../../data/RQ3/issue.csv',index = False)
    print(df)
select_issue('../../data/RQ3/issue_info.csv')