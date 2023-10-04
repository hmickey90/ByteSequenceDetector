import pandas as pd

# 读取 CSV 文件，假设文件名为 'data.csv'
df = pd.read_csv('/home/mickey/Documents/CSV/mal.csv')

# 指定要检查重复的列名，例如 'column_name'
column_name = 'file'

# 使用 count() 函数计算指定列的重复值数量
duplicate_count = df[column_name].duplicated().sum()

# 打印出重复值数量
print(f'The number of duplicates in {column_name} is: {duplicate_count}')