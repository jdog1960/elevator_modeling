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
        psgr['id'] = f"psgr{i}"
        floor1 = random.randint(1,floors)
        floor2 = random.choice([f for f in range(1,floors) if f != floor1])
        psgr_dir = choose_direction()
        if psgr_dir == 1:
            psgr['source'],psgr['dest'] = floor1, floor2
        else:
            psgr['source'],psgr['dest'] = floor2, floor1
        sim_list.append(psgr)
        # print(psgr)

    with open(sim_list_filename, 'w') as sim_list_file:
        json.dump(sim_list,sim_list_file)

    return sim_list_filename
        

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

    print(build_simulation_list(floors, psgrs, time))


if __name__ == "__main__":
    main()
