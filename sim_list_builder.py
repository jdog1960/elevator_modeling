import numpy as np
from datetime import datetime
import json


def build_simulation_list(floors:int, psgrs:int, max_time:int) -> str:
    
    psgrs_20_pct = int(.2 * psgrs)
    psgrs_10_pct = int(.1 * psgrs)
    psgrs_remain = psgrs - (3 * psgrs_20_pct) - (2 * psgrs_10_pct)

    psgr_types = [{'psgr_type':'morning_rush','psgrs':psgrs_20_pct,'time_range':[0,.1*max_time]},
                    {'psgr_type':'evening_rush','psgrs':psgrs_20_pct,'time_range':[.9*max_time,max_time]},
                    {'psgr_type':'pre_lunch','psgrs':psgrs_10_pct,'time_range':[.45*max_time,.5*max_time]},
                    {'psgr_type':'post_lunch','psgrs':psgrs_10_pct,'time_range':[.5*max_time,.55*max_time]},
                    {'psgr_type':'off_times_am','psgrs':psgrs_20_pct,'time_range':[.1*max_time,.45*max_time]},
                    {'psgr_type':'off_times_pm','psgrs':psgrs_remain,'time_range':[.55*max_time,.9*max_time]}]

    time_str = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    sim_list_filename = f"input/simulation_list_{time_str}.json"
    sim_list = []
    
    for p in psgr_types:
        for i in range(p['psgrs']):
            sim_list.append(create_passenger(i, floors, max_time, p))

    with open(sim_list_filename, 'w') as sim_list_file:
        json.dump(sim_list,sim_list_file)

    print(sim_list)
    return sim_list_filename


def create_passenger(i:int, floors:int, max_time:int, psgr_type:dict) -> dict:

    print("creating passenger...")
    psgr_dict = {}
    psgr_dict['time'] = get_time_tick(psgr_type)
    psgr_dict['source'] = get_source_floor(floors, psgr_type)
    psgr_dict['dest'] = get_dest_floor(psgr_dict['source'], floors, psgr_type)
    psgr_dict['id'] = f"psgr_{psgr_type['psgr_type']}_{i}"
    print(f"created passenger {psgr_dict}")
    return psgr_dict


def get_time_tick(psgr_type:dict) -> int:
    time_tick = 0
    rng = np.random.default_rng()

    if psgr_type['psgr_type']=='morning_rush':
        time_tick = int(np.random.triangular(psgr_type['time_range'][0],
                                                         psgr_type['time_range'][0] + 1,
                                                         psgr_type['time_range'][1]))
    elif psgr_type['psgr_type']=='evening_rush':
        time_tick = int(np.random.triangular(psgr_type['time_range'][0],
                                                         psgr_type['time_range'][1] - 1,
                                                         psgr_type['time_range'][1]))
    else:
        time_tick = int(rng.integers(psgr_type['time_range'][0],
                                psgr_type['time_range'][1] + 1))
    
    return time_tick


def get_source_floor(floors:int, psgr_type:dict):
    floor_num = 0
    rng = np.random.default_rng()

    if psgr_type['psgr_type']=='morning_rush' or psgr_type['psgr_type']=='post_lunch':
        floor_num = 1
    else:
        floor_num = int(rng.integers(2,floors + 1))

    return floor_num


def get_dest_floor(source_floor:int, floors:int, psgr_type:dict):
    floor_num = 0
    
    if psgr_type['psgr_type']=='evening_rush' or psgr_type['psgr_type']=='pre_lunch':
        floor_num = 1
    else:
        floor_num = int(np.random.choice(list(set([x for x in range(2,floors + 1)]) - set([source_floor]))))

    return floor_num


def main():
    floors = 10
    psgrs = 20
    time = 15

    print(build_simulation_list(floors, psgrs, time))


if __name__ == "__main__":
    main()
