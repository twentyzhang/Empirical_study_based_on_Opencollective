import pandas as pd

# 加载两个CSV文件
df1 = pd.read_csv('../../data/RQ3/sponsor_info.csv')  # 替换为你的第一个CSV文件的路径
df2 = pd.read_csv('../../data/RQ3/regression_data_base.csv')  # 替换为你的第二个CSV文件的路径

# 将df2中的 'Base' 列从 'year-month' 格式（如 '2023-04'）转换为 'month-year' 格式，以匹配df1
df2['Base'] = pd.to_datetime(df2['Base'], format='%Y-%m').dt.strftime('%b-%y')

# 根据 'Slug' 和 'Base' 列对两个DataFrame进行合并
merged_df = pd.merge(df1, df2, on=['Slug', 'Base','Month'], how='inner')
merged_df.to_csv('../../data/RQ3/regression_data.csv', index=False)  # 保存路径为 'merged_file.csv'
# 显示合并后的DataFrame
print(merged_df)
