
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
    elevator['passengers'].append(psgr)
    elevator['requests'] = [p for p in elevator['requests'] if p['id']!=psgr['id']]
    refresh_target_floor_list(elevator)
    psgr['status'] = "riding"


def unload_passenger(elevator:dict,psgr:dict):
    print(f"unloading passenger {psgr['id']} from elevator {elevator['name']}")
    elevator['passengers'] = [p for p in elevator['passengers'] if p['id']!=psgr['id']]
    refresh_target_floor_list(elevator)
    psgr['status'] = 'complete'


def refresh_target_floor_list(elevator:dict):
    elevator['target_floors'] = [p['dest'] for p in elevator['passengers']]
    elevator['target_floors'].extend([p['source'] for p in elevator['requests']])
    