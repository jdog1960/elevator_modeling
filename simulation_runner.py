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
    if num_floors <= 2:
        print('number of floors must be greater than 2')
        return
    
    if num_elevators <= 1:
        print('number of elevators must be greater than 1')
        return
    
    b = {}
    b['floors'] = num_floors
    b['elevators'] = []
    for i in range(num_elevators):
        b['elevators'].append(create_elevator(i,elevator_capacity))
    return b


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--floors", help="the number of floors in building", type=int)
    parser.add_argument("-e", "--elevators", help="the number of elevators in building", type=int)
    parser.add_argument("-c", "--capacity", help="the elevator capacity", type=int)
    parser.add_argument("-a", "--algorithm", help="the type of algorithm to use for requests", type=str)
    parser.add_argument("-p", "--passengers", help="number of passengers to run through simulator", type=int)
    parser.add_argument("-t", "--time", help="max time for an elevator request", type=int)

    # initialize simulation
    args = parser.parse_args()
    time_str = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    sim_file_name = build_simulation_list(args.floors, args.passengers, args.time)
    results_file_name = f"output/results_elevators_{time_str}.csv"
    passenger_stats_filename = f"output/passenger_stats_{time_str}.csv"
    algorithm_to_use = args.algorithm

    sim_building = create_building(args.floors, args.elevators, args.capacity)
    active_passengers = 0
    # calculate max time simulator will need to run
    max_time = args.floors*args.elevators
    
    with open(sim_file_name, 'r') as sim_file:
        sim_list = json.load(sim_file)
        max_request = max(sim_list, key=lambda p: p['time'])
        max_time += max_request['time']
    
    # run simulator through time until no more passengers to serve 
    for t in range(max_time):
        print(f"starting time {str(t)} iteration")
        
        # first, move elevator if it has passengers or requests
        # should be no movement at time zero since no passengers or requests yet
        for e in sim_building['elevators']:
            print(f"{e['name']} has {len(e['passengers'])} passengers and {len(e['requests'])} requests, was on floor {e['curr_floor']}, direction {e['curr_direction']}")
            if len(e['passengers'])==0 and len(e['requests'])==0:
                print(f"elevator {e['name']} is still on floor {e['curr_floor']}")
            else:
                e['curr_floor'] += e['curr_direction']
                print(f"{e['name']} is now on floor {e['curr_floor']}")

            # second, elevators unload and then load passengers based on current floor
            # unload first
            if len(e['passengers']):
                print(f"unloading riders for elevator {e['name']}")
                for p in e['passengers']:
                    if p['dest'] == e['curr_floor']:
                        unload_passenger(e,p)
                        active_passengers+=-1
                        p['end_time'] = t
                        with open(passenger_stats_filename,'a') as passenger_stats_file:
                            passenger_stats_file.write(f"{p['id']},{p['source']},{p['dest']},{p['request_time']},{p['start_time']},{p['end_time']},{e['name']}\n")
            else:
                print(f"no passengers to unload for elevator {e['name']}")

        # third, new passengers for current time period make requests
        # and get assigned an elevator
        new_passengers = [p for p in sim_list if p['time']==t]

        if len(new_passengers):
            print(f"{len(new_passengers)} new passengers at time {str(t)}")
            for p in new_passengers:
                p['status'] = "waiting"
                p['request_time'] = t
                assigned_elevator = get_best_elevator(sim_building['elevators'], p, algorithm_to_use)
                add_request(assigned_elevator,p)
                active_passengers+=1
        else:
            print(f"no new passengers at time {str(t)}")

        for e in sim_building['elevators']:
            # load requests and convert them to passengers
            if len(e['requests']):
                print(f"loading riders for elevator {e['name']} on floor {e['curr_floor']}")
                for r in e['requests']:
                    if r['source'] == e['curr_floor']:
                        load_passenger(e,r)
                        r['start_time'] = t
            else:
                print(f"elevator {e['name']} has no passengers to load on floor {e['curr_floor']}")

            # set direction for elevator for next tick of time, based on
            # requests and elevators
            print(f"target floors list: {e['target_floors']}")
            if len(e['requests']) or len(e['passengers']):
                if min(e['target_floors']) > e['curr_floor']:
                    e['curr_direction'] = 1
                    print(f"direction is up; next stop: {min(e['target_floors'])}")
                elif max(e['target_floors']) < e['curr_floor']:
                    e['curr_direction'] = -1
                    print(f"direction is down; next stop: {max(e['target_floors'])}")

            print(f"elevator {e['name']} has {len(e['requests'])} requests and {len(e['passengers'])} riders")

            with open(results_file_name, 'a') as result_file:
                result_file.write(f"{t},{e['name']},{e['curr_floor']},{e['curr_direction']},{len(e['passengers'])},{len(e['requests'])},\"{e['target_floors']}\"\n")
        
        print(f"end of time {t}; active passengers: {active_passengers}")
        # stop simulation when no more active passengers and no future requests in sim file
        future_requests = len([p for p in sim_list if p['time'] > t])
        if active_passengers==0 and future_requests==0:
            print(f"simulation stopped; no new active passengers and no upcoming requests")
            break
    
    print("simulation complete")

if __name__ == "__main__":
    main()