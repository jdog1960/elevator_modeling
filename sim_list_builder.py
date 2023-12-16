import random
from datetime import datetime
import json


def build_simulation_list(floors:int, psgrs:int, max_time:int) -> str:
    
    sim_list = []
    time_str = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    sim_list_filename = f"simulation_list_{time_str}"

    for i in range(psgrs):
        psgr = {}
        psgr['time'] = random.randrange(0, max_time, 1)
        psgr['name'] = f"psgr{i}"
        psgr_dir = choose_direction()
        psgr['source'] = choose_source(floors, psgr_dir)
        psgr['destination'] = choose_destination(floors, psgr['source'], psgr_dir)
        sim_list.append(psgr)
        print(psgr)

    with open(sim_list_filename, 'w') as sim_list_file:
        json.dump(sim_list)
        

    

def choose_direction():
    n = random.randint(1,10)
    return 1 if n > 5 else -1
        

def choose_source(floors:int, direction:int):
    max_floor = floors - 1 if direction == 1 else floors
    return random.randrange(1, max_floor, 1)


def choose_destination(floors:int, 
                       curr_floor:int, 
                       direction:int):
    if direction == 1:
        dest_floor = random.randrange(curr_floor + 1, floors, 1)
    else:
        dest_floor = random.randrange(curr_floor - 1, 1, -1)
        

def main():
    floors = 10
    psgrs = 20
    time = 15

    build_simulation_list(floors, psgrs, time)


if __name__ == "__main__":
    main()
