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
    
    # if all elevators are full
    return elevator_list[0]
        

def get_next_elevator_coming_to_me(elevator_list:list, psgr:dict):
    # print("running same_dir algorithm")
    psgr_direction = 1 if psgr['dest'] > psgr['source'] else -1
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
    
    print(f"no elevators available in same direction for passenger {psgr['id']}")
    
    # alternative 1: find closest empty elevator independent of requests or direction
    empty_list = [e for e in elevator_list if len(e['passengers']) == 0]

    if empty_list:
        empty_list.sort(key = lambda x: get_wait_distance(x, psgr))
        return empty_list[0]

    # alternative 2: get closest non-empty elevator after it drops off last psgr
    non_empty_list = [e for e in elevator_list if len(e['passengers']) > 0]
    non_empty_list.sort(key = lambda x: get_wait_distance_post_empty(x, psgr))
    return non_empty_list[0]
    

def is_elevator_full(elevator:dict, target_floor=None):
    current_load = len(elevator['passengers'])
    print(f"current load for elevator {elevator['name']} is {current_load}")
    getting_off = 0
    getting_on = 0
    
    if target_floor:
        getting_off = get_capacity_changes(elevator, target_floor, "off")
        getting_on = get_capacity_changes(elevator, target_floor, "on")

    return elevator['capacity'] <= current_load - getting_off + getting_on


def get_capacity_changes(elevator:dict, target_floor:int, on_or_off:str):
    dir = elevator['curr_direction']
    psgr_list = elevator['passengers'] if on_or_off == "off" else elevator['requests']
    psgr_field = "source" if on_or_off == "off" else "dest"

    changes_list = [p[psgr_field] for p in psgr_list 
                      if p[psgr_field]*dir > elevator['curr_floor']*dir
                      and p[psgr_field]*dir <= target_floor*dir]

    print(f"elevator {elevator['name']} getting {on_or_off}: {changes_list}")
    return len(changes_list)


def get_wait_distance(elevator:dict, psgr:dict) -> int:
    return abs(psgr['source'] - elevator['curr_floor'])

def get_wait_distance_post_empty(elevator:dict, psgr:dict) -> int:
    """"
        find distance from requesting passenger
        for an elevator 
        after it drops off its last passenger
    """
    psgr_dest_list = [p['dest'] for p in elevator['passengers']]
    terminal_floor = max(psgr_dest_list) if elevator['curr_direction'] == 1 else min(psgr_dest_list)
    return abs(psgr['source'] - terminal_floor)
