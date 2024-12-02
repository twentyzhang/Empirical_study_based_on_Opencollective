import pandas as pd
import re

def extract_twitter_data(input_csv):
    # 读取 CSV 文件
    df = pd.read_csv(input_csv)
    
    # 筛选出带有 Twitter 数据的行
    df_filtered = df[df['Twitter'].notnull() & df['Twitter'].str.startswith("https://twitter.com/")].copy()
    
    # 提取 Twitter 用户名
    df_filtered['Twitter_Username'] = df_filtered['Twitter'].apply(lambda x: re.sub(r"https://twitter.com/", "", x))
    
    # 保留需要的列
    df_filtered = df_filtered[['Id', 'Slug', 'Twitter_Username']]
    
    return df_filtered  # 返回筛选后的数据

def standardize_and_filter(df, output_file):
    # 定义标准化处理函数
    def standardize_name(name):
        # 去除下划线和短横线，并统一大小写
        return re.sub(r"[_\-]", "", name).lower()
    # 对 Slug 和 Twitter_Username 进行标准化处理
    df["Standardized_Slug"] = df["Slug"].apply(standardize_name)
    df["Standardized_Twitter"] = df["Twitter_Username"].apply(standardize_name)
    # 筛选标准化后完全匹配或 Twitter_Username 包含 Slug 的项目
    filtered_df = df[df.apply(lambda row: row["Standardized_Slug"] in row["Standardized_Twitter"], axis=1)]
    # 删除辅助列，只保留原始数据
    filtered_df = filtered_df.drop(columns=["Standardized_Slug", "Standardized_Twitter"])
    # 保存筛选结果
    filtered_df.to_csv(output_file, index=False)
    print(f"筛选完成，结果已保存到 {output_file}")
# 设置输入和输出文件路径
input_csv = "../../data/RQ2/oc.csv"  # 输入的原始 CSV 文件路径
output_csv = "../../data/RQ2/twitter_info.csv"  # 筛选后的最终结果文件路径

# 提取拥有推特账户的项目
df_filtered = extract_twitter_data(input_csv)

# 对筛选后的数据进行标准化和进一步筛选，并保存最终结果
standardize_and_filter(df_filtered, output_csv)
