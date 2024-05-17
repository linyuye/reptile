import pandas as pd

# 读取CSV文件
df = pd.read_csv('xxxxxxx.csv')
cols_to_check = ['昵称', '时间', '评论']

# 删除除了每组重复行中的第一行以外的所有行
unique_df = df.drop_duplicates(subset=cols_to_check, keep='first')

# 将结果保存到新的CSV文件
unique_df.to_csv('123456.csv', index=False, encoding='utf-8-sig')
