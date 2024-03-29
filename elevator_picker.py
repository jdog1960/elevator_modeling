# functions specific to request-elevator matching algorithms
import numpy as np
from elevator import is_elevator_full_at_target, has_max_requests


def get_best_elevator(elevator_list:list, psgr:dict, method_id:str) -> dict:
    # logic to pick the best elevator for current request
    print(f"getting best elevator for {psgr['id']} using method {method_id}...")
    algo_options = {'sl':get_next_elevator_simple_list,
                    'sr':get_next_elevator_simple_random,
                    'sd':get_next_elevator_same_dir}

    return algo_options[method_id](elevator_list,psgr)
 

def get_next_elevator_simple_list(elevator_list:list, psgr:dict=None):
    """
    iterate through the list of elevators to find first available
    if none available pick the first elevator in the list
    """
    for e in elevator_list:
        if is_elevator_full_at_target(e, psgr['source']):
            print(f"elevator {e['name']} will be full at pickup of {psgr['id']}")
        else:
            return e
    
    # if all elevators are full, pick first one
    return elevator_list[0]


def get_next_elevator_simple_random(elevator_list:list, psgr:dict):
    """
    mix up list of elevators before iterating to pick the first
    available one, if all full add request to a random elevator
    in the list
    """
    np.random.shuffle(elevator_list)

    for e in elevator_list:
        if is_elevator_full_at_target(e, psgr['source']) or has_max_requests(e):
            print(f"elevator {e['name']} will be full or too many requests")
        else:
            return e
    
    # if all elevators are full, pick one at random
    rng = np.random.default_rng()
    i = rng.integers(0, len(elevator_list) - 1)
    return elevator_list[i]
        

def get_next_elevator_same_dir(elevator_list:list, psgr:dict) -> dict:
    """
        Find best elevator based on multiple criteria:
        - is it going same direction?
        - has it passed my request floor already?
        - if some fit, sort by distance from request floor
        - 
    """
    psgr_direction = 1 if psgr['dest'] > psgr['source'] else -1
    # narrow to only elevators going in same direction
    pick_list = [e for e in elevator_list if e['curr_direction'] == psgr_direction]
    print(f"pick list length after removing wrong direction: {len(pick_list)}")
    if pick_list:
        pick_list = [e for e in pick_list if e['curr_floor']*psgr_direction < psgr['source']*psgr_direction]
        print(f"pick list length after removing already passed: {len(pick_list)}")
        if pick_list:
            pick_list.sort(key=lambda x: get_wait_distance(x, psgr))
            print([e['name'] for e in pick_list])

            for e in pick_list:
                if is_elevator_full_at_target(e, psgr['source']):
                    print(f"elevator {e['name']} is full at time of pickup")
                else:
                    return e
        else:
            print("no elevators going same direction and on way to psgr")
    else:
        print("no elevators going same direction")

    print(f"no elevators available in same direction for and on way to passenger {psgr['id']}")
    # if none available in same direction and on way to psgr, get elevator with least requests:
    return get_elevator_least_demands(elevator_list)


def get_next_elevator_closest_one(elevator_list:list, psgr:dict) -> dict:
    """
        look for closest empty elevator first,
        then look for closest non-full elevator,

    """
    best_elevator = get_closest_empty_elevator(elevator_list, psgr)
    if best_elevator:
        return best_elevator
    else:
        best_elevator = get_closest_elevator_with_space(elevator_list, psgr)
        if best_elevator:
            return best_elevator
        else:
            return best_elevator


def get_closest_empty_elevator(elevator_list:list, psgr:dict) -> dict:
    # step 1:  look for any empty elevator and send it to psgr
    empty_no_request_list = [e for e in elevator_list 
                            if len(e['passengers']) == 0
                            and len(e['requests']) == 0]

    if empty_no_request_list:
        empty_no_request_list.sort(key = lambda x: get_wait_distance(x, psgr))
        return empty_no_request_list[0]
    return None

def get_closest_elevator_with_space(elevator_list:list, psgr:dict) -> dict:
    non_empty_list = [e for e in elevator_list if not is_elevator_full_at_target(e, psgr['source'])]
    if non_empty_list:
        non_empty_list.sort(key = lambda x: get_wait_distance_post_empty(x, psgr))
        return non_empty_list[0]
    return None


def get_wait_distance(elevator:dict, psgr:dict) -> int:
    return abs(psgr['source'] - elevator['curr_floor'])


def get_wait_distance_post_empty(elevator:dict, psgr:dict) -> int:
    """"
        find distance from requesting passenger
        for an elevator 
        after it drops off its last passenger
    """
    psgr_dest_list = [p['dest'] for p in elevator['passengers']]

    if psgr_dest_list:
        terminal_floor = max(psgr_dest_list) if elevator['curr_direction'] == 1 else min(psgr_dest_list)
        return abs(psgr['source'] - terminal_floor)
    else:
        return abs(psgr['source'] - elevator['curr_floor'])


def get_elevator_least_demands(elevator_list:list) -> dict:
    """find elevator with smallest number of passengers and requests combined"""
    elevator_list.sort(key = lambda e: len(e['target_floors']))
    return elevator_list[0]