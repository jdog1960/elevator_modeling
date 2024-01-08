import pandas as pd

def analyse_passenger_stats(file_name:str, first_in_line:bool):
    algorithm_id = file_name[:2]
    df_passenger_stats = pd.read_csv(f"output/{file_name}",
                                    header=None)

    df_passenger_stats.columns = ["psgr","source","dest","request_time","start_time","end_time","elevator"]
    df_passenger_stats['alg_id'] = algorithm_id
    df_passenger_stats['distance'] = abs(df_passenger_stats['dest'] - df_passenger_stats['source'])
    df_passenger_stats['wait_time'] = df_passenger_stats['start_time'] - df_passenger_stats['request_time']
    df_passenger_stats['ride_time'] = df_passenger_stats['end_time'] - df_passenger_stats['start_time']
    df_passenger_stats['total_time'] = df_passenger_stats['end_time'] - df_passenger_stats['request_time']
    df_passenger_stats['ride_ratio'] = df_passenger_stats['ride_time']/df_passenger_stats['distance']

    df_compare_psgrs = df_passenger_stats[['alg_id','elevator','psgr','distance','wait_time','ride_time','total_time','ride_ratio']]
    agg_dict = {'psgr':'count','distance':'mean','wait_time':'mean','ride_time':'mean','total_time':'mean','ride_ratio':'mean'}
    df_compare_psgrs_by_elevator = df_compare_psgrs.groupby(['alg_id','elevator']).aggregate(agg_dict)    
    df_compare_psgrs_by_elevator.to_csv('output/passenger_analysis.csv', mode='a', header=first_in_line, index=True)


def main(file_name:str, first_in_line:bool):
    analyse_passenger_stats(file_name, first_in_line)

if __name__=='__main__':
    main('sd_passenger_stats_2024_01_05_215057.csv', first_in_line=True)