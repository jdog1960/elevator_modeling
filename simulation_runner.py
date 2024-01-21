import json
from datetime import datetime
from argparse import ArgumentParser
from sim_list_builder import build_simulation_list
from elevator import create_elevator, add_request, load_passenger, unload_passenger
from elevator_picker import get_best_elevator


def create_building(num_floors:int, num_elevators:int, elevator_capacity:int) -> dict:
    print(f"""creating building with {num_floors} floors, 
          {num_elevators} elevators, 
          {elevator_capacity} passengers per elevator""")
    
    # validate building first
    if not validate_building(num_floors, num_elevators, elevator_capacity):
        return(f"elevator not valid")
    
    b = {}
    b['floors'] = num_floors
    b['elevators'] = []
    for i in range(num_elevators):
        b['elevators'].append(create_elevator(i,elevator_capacity))
    return b


def validate_building(num_floors:int, num_elevators:int, capacity:int) -> int:
    
    if num_floors <= 2:
        print('number of floors must be greater than 2')
        return False
    
    if num_elevators <= 1:
        print('number of elevators must be greater than 1')
        return False
    
    if capacity <= 1:
        print('elevator capacity must be greater than 1')
        return False
    
    return True
    

def move_to_next_floor_or_stay(elevator:dict):
    print(f"""{elevator['name']} has {len(elevator['passengers'])} passengers 
          and {len(elevator['requests'])} requests, 
          was on floor {elevator['curr_floor']}, 
          direction {elevator['curr_direction']}""")
    if len(elevator['passengers'])==0 and len(elevator['requests'])==0:
        print(f"elevator {elevator['name']} is still on floor {elevator['curr_floor']}")
    else:
        elevator['curr_floor'] += elevator['curr_direction']
        print(f"{elevator['name']} is now on floor {elevator['curr_floor']}")


def unload_passengers(elevator:dict, time:int, psgr_stats_file_name:str):
    """unload any passengers at their target floor"""
    if len(elevator['passengers']):
        print(f"unloading riders for elevator {elevator['name']}")
        for p in elevator['passengers']:
            if p['dest'] == elevator['curr_floor']:
                unload_passenger(elevator,p)
                p['end_time'] = time
                with open(psgr_stats_file_name,'a') as passenger_stats_file:
                    passenger_stats_file.write(f"{p['id']},{p['source']},{p['dest']},{p['request_time']},{p['start_time']},{p['end_time']},{elevator['name']}\n")
    else:
        print(f"no passengers for elevator {elevator['name']}")


def passengers_push_button(psgr_list:list, 
                            elevator_list:list, 
                            time:int,
                            algorithm:str):
    if len(psgr_list):
        print(f"{len(psgr_list)} new passengers at time {str(time)}")
        for p in psgr_list:
            p['status'] = "waiting"
            p['request_time'] = time
            assigned_elevator = get_best_elevator(elevator_list, p, algorithm)
            add_request(assigned_elevator, p)
    else:
        print(f"no new passengers at time {str(time)}")


def onboard_passengers(elevator:dict, time:int):
    if len(elevator['requests']):
        print(f"loading riders for elevator {elevator['name']} on floor {elevator['curr_floor']}")
        for r in elevator['requests']:
            if r['source'] == elevator['curr_floor']:
                load_passenger(elevator,r)
                r['start_time'] = time
    else:
        print(f"""elevator {elevator['name']} has no passengers 
              to load on floor {elevator['curr_floor']}""")


def set_direction_for_next_tick(elevator:dict):
    if len(elevator['requests']) or len(elevator['passengers']):
        if min(elevator['target_floors']) > elevator['curr_floor']:
            elevator['curr_direction'] = 1
            print(f"direction is up; next stop: {min(elevator['target_floors'])}")
        elif max(elevator['target_floors']) < elevator['curr_floor']:
            elevator['curr_direction'] = -1
            print(f"direction is down; next stop: {max(elevator['target_floors'])}")


def log_elevator_stats(elevator:dict, results_file_name:str, time:int):
    print(f"elevator {elevator['name']} has {len(elevator['requests'])} requests and {len(elevator['passengers'])} riders")
    with open(results_file_name, 'a') as result_file:
        result_file.write(f"""{time},{elevator['name']},{elevator['curr_floor']},{elevator['curr_direction']},{len(elevator['passengers'])},{len(elevator['requests'])},\"{elevator['target_floors']}\"\n""")


def main(floors:int,
         elevators:int,
         capacity:int,
         algorithm:str,
         passengers:int,
         sim_file_name:str):
    
    # initialize simulation
    time_str = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    results_file_name = f"output/{algorithm}_results_elevators_{time_str}.csv"
    passenger_stats_filename = f"output/{algorithm}_passenger_stats_{time_str}.csv"
    sim_building = create_building(floors, elevators, capacity)
    elevator_list = sim_building['elevators']
    # calculate max time simulator will need to run
    max_time = floors*passengers
    

    with open(sim_file_name, 'r') as sim_file:
        sim_list = json.load(sim_file)
        max_request = max(sim_list, key=lambda p: p['time'])
        max_time += max_request['time']
    
    # run simulator through time until no more passengers to serve 
    for t in range(max_time):
        print(f"starting time {str(t)} iteration")
        
        for e in elevator_list:
            move_to_next_floor_or_stay(e)
            unload_passengers(e, t, passenger_stats_filename)

        new_passengers = [p for p in sim_list if p['time']==t]
        passengers_push_button(new_passengers, 
                                elevator_list, 
                                t,
                                algorithm)

        active_passengers=0
        for e in elevator_list:
            onboard_passengers(e, t)
            set_direction_for_next_tick(e)
            log_elevator_stats(e, results_file_name, t)
            active_passengers+=len(e['requests']) + len(e['passengers'])

        print(f"end of time {t}; active passengers: {active_passengers}")
        # stop simulation when no more active passengers and no future requests in sim file
        if active_passengers==0 and t > max(sim_list, key=lambda x:x['time'])['time']:
            print(f"simulation stopped; no new active passengers and no more sim time ticks")
            break
    
    print(f"simulation complete for algorithm {algorithm}")


if __name__ == "__main__":
    # running this file directly will always generate a new, different simuliation file
    parser = ArgumentParser()
    parser.add_argument("-f", "--floors", help="the number of floors in building", type=int)
    parser.add_argument("-e", "--elevators", help="the number of elevators in building", type=int)
    parser.add_argument("-c", "--capacity", help="the elevator capacity", type=int)
    parser.add_argument("-a", "--algorithm", help="the type of algorithm to use for requests", type=str)
    parser.add_argument("-p", "--passengers", help="number of passengers to run through simulator", type=int)
    parser.add_argument("-t", "--time", help="max time for an elevator request", type=int)

    args = parser.parse_args()
    sim_file_name = build_simulation_list(args.floors, args.passengers, args.time)
    
    main(args.floors,
         args.elevators,
         args.capacity,
         args.algorithm,
         args.passengers,
         sim_file_name)