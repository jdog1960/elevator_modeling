import pandas as pd

# passenger waiting and travel
df_passenger_stats = pd.read_csv("output/passenger_stats_2023_12_17_214210.csv",
                                 header=None)
df_passenger_stats.columns = ["id","source","dest","request_time","start","end","elevator"]
df_passenger_stats['distance'] = abs(df_passenger_stats['dest'] - df_passenger_stats['source'])
df_passenger_stats['wait'] = df_passenger_stats['start'] - df_passenger_stats['request_time']
df_passenger_stats['ride'] = df_passenger_stats['end'] - df_passenger_stats['start']
df_passenger_stats['ride_ratio'] = df_passenger_stats['ride']/df_passenger_stats['distance']
df_passenger_stats['total'] = df_passenger_stats['wait'] + df_passenger_stats['ride']
print(df_passenger_stats)

print(f"min wait: {df_passenger_stats['wait'].min()}")
print(f"max wait: {df_passenger_stats['wait'].max()}")
print(f"mean wait: {df_passenger_stats['wait'].mean()}")
print(f"median wait: {df_passenger_stats['wait'].median()}")
print(f"mean ride ratio: {df_passenger_stats['ride_ratio'].mean()}")
print(f"median ride ratio: {df_passenger_stats['ride_ratio'].median()}")



