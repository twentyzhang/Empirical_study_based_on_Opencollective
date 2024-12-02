import pandas as pd

# 读取第一个 CSV 文件并按 'OpenCollective' 分组汇总
input_file = '../../data/RQ2/repo.csv'
output_file = '../../data/RQ2/data.csv'

df = pd.read_csv(input_file)

# 按照 'OpenCollective' 分组并求和
grouped_df = df.groupby('OpenCollective').agg({
    'Stars': 'sum',
    'Forks': 'sum',
    'Watcher': 'sum',
    'Issue': 'sum',
    'PullRequest': 'sum',
    'Release': 'sum',
    'DiskUsage': 'sum'
}).reset_index()
# 重命名 'OpenCollective' 列为 'Slug'
grouped_df.rename(columns={'OpenCollective': 'Slug'}, inplace=True)
# 加载已经部分合并的数据，用于进一步的合并
df2 = pd.read_csv('../../data/RQ2/RQ2_data.csv')
# 合并两个 DataFrame，基于 'Slug' 列
merged_df = pd.merge(grouped_df, df2, on=['Slug'], how='inner')

# 合并推特账户信息
df_twitter = pd.read_csv('../../data/RQ2/twitter_data.csv')

df_twitter = df_twitter.dropna(subset=['Slug'])
# 创建一个 'hasTwitter' 列，默认值为 0
merged_df['hasTwitter'] = merged_df['Slug'].isin(df_twitter['Slug']).astype(int)
# 保存最终结果到 CSV 文件
merged_df.to_csv(output_file, index=False)

print(f"合并后的数据已保存到 {output_file}")
