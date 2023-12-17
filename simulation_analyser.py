import pandas as pd

# passenger waiting and travel
df_passenger_stats = pd.read_csv("passenger_stats_2023_12_14_221521.csv",
                                 header=None)
df_passenger_stats.columns = ["id","source","dest","request","start","end"]
df_passenger_stats['distance'] = abs(df_passenger_stats['dest'] - df_passenger_stats['source'])
df_passenger_stats['wait'] = df_passenger_stats['start'] - df_passenger_stats['request']
df_passenger_stats['ride'] = df_passenger_stats['end'] - df_passenger_stats['start']

print(df_passenger_stats)


