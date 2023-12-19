# functions specific to request-elevator matching algorithms
import random
from elevator import is_elevator_full_now, is_elevator_full_at_target, has_max_requests

def get_best_elevator(elevator_list:list, psgr:dict, method_id:str) -> dict:
    # logic to pick the best elevator for current request
    print(f"getting best elevator for {psgr['id']} using method {method_id}...")

    if method_id == "simple_list":
        return get_next_elevator_simple_list(elevator_list)
    if method_id == "simple_random":
        return get_next_elevator_simple_random(elevator_list)
    if method_id == "same_dir":
        return get_next_elevator_same_dir(elevator_list, psgr)


def get_next_elevator_simple_list(elevator_list:list):
    # print(f"running simple_list algorithm")
    for e in elevator_list:
        if is_elevator_full_now(e):
            print(f"elevator {e['name']} is full")
        else:
            return e
    
    # if all elevators are full, pick first one
    return elevator_list[0]


def get_next_elevator_simple_random(elevator_list:list):
    # print(f"running simple_list algorithm")
    for e in elevator_list:
        if is_elevator_full_now(e) or has_max_requests(e):
            print(f"elevator {e['name']} is full or lots of requests")
        else:
            return e
    
    # if all elevators are full, pick one at random
    return elevator_list[random.randint(0, len(elevator_list)-1)]
        

def get_next_elevator_same_dir(elevator_list:list, psgr:dict):
    """
        Find best elevator based on multiple criteria:
        - is it going same direction?
        - has it passed my request floor already?
        - if none fit, fall back to simple list picker
        - if some fit, sort by distance from request floor
        - 
    """
    # print("running same_dir algorithm")
    psgr_direction = 1 if psgr['dest'] > psgr['source'] else -1
    # narrow to only elevators going in same direction
    pick_list = [e for e in elevator_list if e['curr_direction'] == psgr_direction]
    print(f"pick list length after removing wrong direction: {len(pick_list)}")
    if len(pick_list):
        pick_list = [e for e in pick_list if e['curr_floor']*psgr_direction > psgr['source']*psgr_direction]
        print(f"pick list length after removing already passed: {len(pick_list)}")
    # if none in same direction, bail out to simple list
    if len(pick_list)==0:
        print("no elevators going same direction and on way to psgr")
        return get_next_elevator_simple_list(elevator_list)
    # iterate through list in order of closeness to psgr, assign first one
    # that won't be full on arrival at psgr source floor
    pick_list.sort(key=lambda x: get_wait_distance(x, psgr))
    print([e['name'] for e in pick_list])

    for e in pick_list:
        if is_elevator_full_at_target(e, psgr['source']):
            print(f"elevator {e['name']} is full at time of pickup")
        else:
            return e
    
    print(f"no elevators available in same direction for passenger {psgr['id']}")
    
    # alternative 1: find closest empty elevator independent of requests or direction
    empty_no_request_list = [e for e in elevator_list 
                            if len(e['passengers']) == 0
                            and len(e['requests']) == 0]

    if empty_no_request_list:
        empty_no_request_list.sort(key = lambda x: get_wait_distance(x, psgr))
        return empty_no_request_list[0]

    # alternative 2: get closest non-empty elevator after it drops off last psgr
    non_empty_list = [e for e in elevator_list if len(e['passengers']) > 0]
    non_empty_list.sort(key = lambda x: get_wait_distance_post_empty(x, psgr))
    return non_empty_list[0]
    

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
