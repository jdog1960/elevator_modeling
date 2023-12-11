
def create_elevator(id:int, capacity:int) -> dict:
    elevator = {}
    elevator['name'] = f"elevator{str(id)}"
    elevator['capacity'] = capacity
    elevator['curr_floor'] = 1
    elevator['curr_direction'] = 0
    elevator['passengers'] = []
    elevator['requests'] = []
    elevator['target_floors'] = []
    return elevator

    
def add_request(elevator:dict, psgr:dict):
    print(f"adding request from {psgr['id']} for elevator {elevator['name']}")
    elevator['requests'].append(psgr)
    elevator['target_floors'].append(psgr['source'])
        
    
def load_passenger(elevator:dict,psgr:dict):
    print(f"loading passenger {psgr['id']} on elevator {elevator['name']}")
    if len(elevator['passengers'])<elevator['capacity']:
        elevator['passengers'].append(psgr)
        elevator['requests'] = [p for p in elevator['requests'] if p['id']!=psgr['id']]
        elevator['target_floors'].append(psgr['dest'])
        # remove request source floor from target list
        elevator['target_floors'] = [f for f in elevator['target_floors'] if f!=psgr['source']]
        psgr['status'] = "riding"
    else:
        print(f"elevator {elevator['name']} is full")


def unload_passenger(elevator:dict,psgr:dict):
    print(f"unloading passenger {psgr['id']} from elevator {elevator['name']}")
    elevator['passengers'] = [p for p in elevator['passengers'] if p['id']!=psgr['id']]
    elevator['target_floors'] = [f for f in elevator['target_floors'] if f!=psgr['dest']]
    psgr['status'] = 'complete'