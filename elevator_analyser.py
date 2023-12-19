import pandas as pd

df_elevator_stats = pd.read_csv("output/results_elevators_2023_12_17_214210.csv",
                                 header=None)

df_elevator_stats.columns = ["time","name","curr_floor","curr_direction","passengers","requests","target_floors"]

elevator_list = df_elevator_stats.name.unique()
df_compare_elevators = pd.DataFrame(columns=['elevator',
                                             'elapsed_time',
                                             'max_floor_reached',
                                             'time_going_up',
                                             'time_going_down',
                                             'mean_passengers',
                                             'mean_requests'])

for e in elevator_list:
    one_elevator_stats = {}
    one_elevator_stats['elevator'] = e
    df_one_elevator = df_elevator_stats[df_elevator_stats['name'] == e]
    one_elevator_stats['elapsed_time'] = df_one_elevator['time'].max() + 1
    one_elevator_stats['max_floor_reached'] = df_one_elevator['curr_floor'].max()
    one_elevator_stats['time_going_up'] = df_one_elevator[df_one_elevator['curr_direction']==1].shape[0]
    one_elevator_stats['time_going_down'] = df_one_elevator[df_one_elevator['curr_direction']==-1].shape[0]
    one_elevator_stats['mean_passengers'] = df_one_elevator['passengers'].mean()
    one_elevator_stats['mean_requests'] = df_one_elevator['requests'].mean()
    
    one_elevator_df = pd.DataFrame([one_elevator_stats])
    df_compare_elevators = pd.concat([df_compare_elevators, one_elevator_df])

df_compare_elevators.to_csv('output/elevator_analysis.csv', index=False)
