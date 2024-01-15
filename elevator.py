# elevator-specific functions

def create_elevator(id:int, capacity:int) -> dict:
    elevator = {}
    elevator['name'] = f"elevator{str(id)}"
    elevator['capacity'] = capacity
    elevator['curr_floor'] = 1
    elevator['curr_direction'] = 1
    elevator['passengers'] = []
    elevator['requests'] = []
    elevator['target_floors'] = []
    return elevator

    
def add_request(elevator:dict, psgr:dict):
    print(f"adding request from {psgr['id']} for elevator {elevator['name']}")
    elevator['requests'].append(psgr)
    refresh_target_floor_list(elevator)
        
    
def load_passenger(elevator:dict,psgr:dict):
    print(f"loading passenger {psgr['id']} on elevator {elevator['name']}")
    if is_elevator_full_now(elevator) == False:
        elevator['passengers'].append(psgr)
        elevator['requests'] = [p for p in elevator['requests'] if p['id']!=psgr['id']]
        refresh_target_floor_list(elevator)
    else:
        print(f"can't load {psgr['id']}, no room on elevator")


def unload_passenger(elevator:dict,psgr:dict):
    print(f"unloading passenger {psgr['id']} from elevator {elevator['name']}")
    elevator['passengers'] = [p for p in elevator['passengers'] if p['id']!=psgr['id']]
    refresh_target_floor_list(elevator)


def refresh_target_floor_list(elevator:dict):
    elevator['target_floors'] = [p['dest'] for p in elevator['passengers']]
    elevator['target_floors'].extend([p['source'] for p in elevator['requests']])


def is_elevator_full_now(elevator:dict) -> bool:
    current_load = len(elevator['passengers'])
    print(f"current load for elevator {elevator['name']} is {current_load}")
    return elevator['capacity'] <= current_load


def is_elevator_full_at_target(elevator:dict, target_floor:int) -> bool:
    current_load = len(elevator['passengers'])
    print(f"current load for elevator {elevator['name']} is {current_load}")
    getting_off = get_capacity_changes(elevator, target_floor, "off")
    getting_on = get_capacity_changes(elevator, target_floor, "on")
    return elevator['capacity'] <= current_load - getting_off + getting_on


def get_capacity_changes(elevator:dict, target_floor:int, on_or_off:str) -> int:
    """
        calculate projected occupancy of elevator at target floor
        based on passengers getting off and passenger requests
        boarding - if request is boarding on way to target, make sure
        passenger will not get off before arrival at target
    """
    dir = elevator['curr_direction']
    psgr_list = elevator['passengers'] if on_or_off == "off" else elevator['requests']
    psgr_field = "source" if on_or_off == "off" else "dest"

    changes_list = [p for p in psgr_list 
                      if p[psgr_field]*dir > elevator['curr_floor']*dir
                      and p[psgr_field]*dir <= target_floor*dir]
    
    print(f"elevator {elevator['name']} getting {on_or_off}: {changes_list}")
    return len(changes_list)


def has_max_requests(elevator:dict) -> bool:
    """return true if request count >= elevator's capacity"""
    return len(elevator['requests']) >= elevator['capacity']