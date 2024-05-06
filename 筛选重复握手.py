import pandas as pd
# 读取CSV文件
df = pd.read_csv('2_2_test.csv')
cols_to_check = ['昵称', '时间', '评论']  # 替换'另一列'为实际的列名
# 使用duplicated方法检查这些列的组合是否重复，keep=False表示考虑所有重复项
# 然后使用~操作符取反，得到仅出现一次的行的布尔掩码
unique_mask = ~df[cols_to_check].duplicated(keep=False)
# 使用布尔掩码来筛选仅出现一次的行
unique_df = df[unique_mask]
unique_df.to_csv('unique_rows.csv', index=False, encoding='utf-8-sig')
