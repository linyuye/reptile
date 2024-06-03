import pandas as pd

# 读取CSV文件
df = pd.read_csv('xxxxxxxxxxxxxxx.csv', dtype={'rpid': str})
cols_to_check = ['昵称', '时间', '评论']
BV = "BV1305035422/"

# 使用.copy()确保unique_df是一个独立的副本
unique_df = df.drop_duplicates(subset=cols_to_check, keep='first').copy()

# 因为在读取时已经指定了dtype={'rpid': str}，所以这一步可能是多余的
unique_df['rpid'] = unique_df['rpid'].astype(str)

# 构造新列
unique_df['新列'] = 'https://www.bilibili.com/video/' +  BV  + '#reply' + unique_df['rpid'].fillna('')

# 将结果保存到新的CSV文件
unique_df.to_csv('comments/绝区零1.2w标准数据.csv', index=False, encoding='utf-8-sig')
