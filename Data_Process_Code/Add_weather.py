from idlelib.iomenu import encoding

import pandas as pd
import os


a_file = r"operation.csv"
b_file = r"historical_weather_data.csv"

if not os.path.exists(a_file):
    raise FileNotFoundError(f"文件 {a_file} 不存在，请检查路径。")

if not os.path.exists(b_file):
    raise FileNotFoundError(f"文件 {b_file} 不存在，请检查路径。")


a_df = pd.read_csv(a_file)
b_df = pd.read_csv(b_file, encoding='gbk')


if a_df.empty:
    raise ValueError("操作.csv 为空，请检查数据内容。")

if b_df.empty:
    raise ValueError("historical_weather_data.csv 为空，请检查数据内容。")


b_df['station'] = b_df['station'].astype(str).str.strip().str.lower()
a_df['match_station'] = a_df['station_name'].astype(str).str.strip().str.lower()


a_df['date'] = pd.to_datetime(a_df['date'], errors='coerce')
b_df['date'] = pd.to_datetime(b_df['date'], errors='coerce')


a_df = a_df.dropna(subset=['date'])
b_df = b_df.dropna(subset=['date'])


merged_df = a_df.merge(
    b_df[['station', 'date', 'temperature_min', 'temperature_max', 'weather_condition']],
    left_on=['match_station', 'date'],
    right_on=['station', 'date'],
    how='left'
)


merged_df.drop(columns=['match_station', 'station'], inplace=True)


if merged_df.empty:
    raise ValueError("合并后数据为空，请检查 `station_name`、`station` 和 `date` 是否匹配正确。")


output_file = "operation.csv"
merged_df.to_csv(output_file, index=False, encoding='utf-8')

