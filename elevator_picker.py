# functions specific to request-elevator matching algorithms

def get_best_elevator(elevator_list:list, psgr:dict, method_id:str) -> dict:
    # logic to pick the best elevator for current request
    print(f"getting best elevator for {psgr['id']} using method {method_id}...")
    
    if method_id == "simple_list":
        return get_next_elevator_in_list(elevator_list)
    if method_id == "same_dir":
        return get_next_elevator_coming_to_me(elevator_list, psgr)


def get_next_elevator_in_list(elevator_list:list):
    # print(f"running simple_list algorithm")
    for e in elevator_list:
        if is_elevator_full(e):
            print(f"elevator {e['name']} is full")
        else:
            return e
        

def get_next_elevator_coming_to_me(elevator_list:list, psgr:dict):
    # print("running same_dir algorithm")
    psgr_direction = 1 if psgr['dest'] - psgr['source'] > 0 else -1
    # narrow to only elevators going in same direction
    pick_list = [e for e in elevator_list if e['curr_direction'] == psgr_direction]
    print(f"pick list length after removing wrong direction: {len(pick_list)}")
    pick_list = [e for e in pick_list if e['curr_floor']*psgr_direction <= psgr['source']*psgr_direction]
    print(f"pick list length after removing already passed: {len(pick_list)}")
    # if none in same direction, bail out to simple list
    if len(pick_list)==0:
        print("no elevators going same direction and on way to psgr")
        return get_next_elevator_in_list(elevator_list)
    # iterate through list in order of closeness to psgr, assign first one
    # that won't be full on arrival at psgr source floor
    pick_list.sort(key=lambda x: get_wait_distance(x, psgr))
    print([e['name'] for e in pick_list])

    for e in pick_list:
        if is_elevator_full(e, psgr['source']):
            print(f"elevator {e['name']} is full at time of pickup")
        else:
            return e
    
    print(f"failed to assign an elevator for passenger {psgr['id']}")


def is_elevator_full(elevator, source_floor=None):
    current_load = len(elevator['passengers']) + len(elevator['requests'])
    unloaded_before_pickup = 0
    print(f"current load for elevator {elevator['name']} is {current_load}")
    dir = elevator['curr_direction']
    if source_floor:
        unloaded_before_pickup = len([f for f in elevator['target_floors'] 
                                      if f*dir > elevator['curr_floor']*dir
                                      and f*dir <= source_floor])
        print(f"unloaded before pickup for elevator {elevator['name']} is {unloaded_before_pickup}")

    return elevator['capacity'] <= current_load - unloaded_before_pickup


def get_wait_distance(elevator:dict, psgr:dict) -> int:
    return abs(psgr['source'] - elevator['curr_floor'])
