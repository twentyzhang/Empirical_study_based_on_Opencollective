import pandas as pd
import numpy as np
# 读取 CSV 文件
commit_info = pd.read_csv('../../data/RQ3/commit.csv')
issue_info = pd.read_csv('../../data/RQ3/issue.csv')
spend_info = pd.read_csv('../../data/RQ3/spend_info.csv')

# 手动为 spend_info 中的非 'Slug' 和 'Base' 列添加 '_spend' 后缀
spend_info = spend_info.rename(columns={col: f"{col}_spend" for col in spend_info.columns if col not in ['Slug', 'Base']})
# 合并数据，仅保留 'Slug' 和 'Base' 在三个文件中都存在的行（内连接）
merged_data = commit_info.merge(issue_info, on=['Slug', 'Base'], suffixes=('_commit', '_issue'), how='inner') \
                         .merge(spend_info, on=['Slug', 'Base'], how='inner')
merged_data_long = pd.melt(
    merged_data,
    id_vars=['Slug', 'Base'],
    var_name='Month_Variable',
    value_name='Value'
)
# 分离 'Month_Variable' 列，提取月份和类型
merged_data_long[['Month', 'Type']] = merged_data_long['Month_Variable'].str.extract(r'(-?\d+)_(\w+)')
# 将 'Month' 转换为整数类型
merged_data_long['Month'] = merged_data_long['Month'].astype(int)
# 删除不再需要的 'Month_Variable' 列
merged_data_long = merged_data_long.drop(columns=['Month_Variable'])
#将 'Type' 列转换为多个列
merged_data_wide = merged_data_long.pivot_table(index=['Slug', 'Base', 'Month'], columns='Type', values='Value').reset_index()
# 查看转换后的数据
print(merged_data_wide)
# 添加 'Intervention' 列：当 Month >= 0 时，设置为 1；否则为 0
merged_data_wide['Intervention'] = merged_data_wide['Month'].apply(lambda x: 1 if x >= 0 else 0)
# 添加 'Time after intervention' 列：当有干预时为 time - 6，干预之前都设置为 0
merged_data_wide['Time_after_intervention'] = merged_data_wide['Month'].apply(lambda x: x  if x >= 0 else 0)
# 数据预处理
merged_data_wide['Commit_log'] = (merged_data_wide['commit'] + 0.5).apply(np.log)
merged_data_wide['Issue_log'] = (merged_data_wide['issue'] + 0.5).apply(np.log)
merged_data_wide['Spend_log'] = (merged_data_wide['spend'] + 0.5).apply(np.log)
print(merged_data_wide)
merged_data_wide.to_csv('../data/modelRegression/baseDatas/regression_data_base.csv', index=False)
