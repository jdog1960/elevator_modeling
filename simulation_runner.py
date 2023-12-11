import json
from argparse import ArgumentParser
from elevator import create_elevator, add_request, load_passenger, unload_passenger


def create_building(num_floors:int, num_elevators:int, elevator_capacity:int) -> dict:
    print(f"""creating building with {num_floors} floors, 
          {num_elevators} elevators, 
          {elevator_capacity} passengers per elevator""")
    b = {}
    b['floors'] = num_floors
    b['elevators'] = []
    for i in range(num_elevators):
        b['elevators'].append(create_elevator(i,elevator_capacity))
        print(f"created elevator {b['elevators'][i]['name']}")
    return b


def get_best_elevator(sim_building:dict, psgr:dict) -> str:
    # logic to pick the best elevator for current request
    print(f"getting best elevator for {psgr['id']}...")
    for e in sim_building['elevators']:
        print(f"{len(e['target_floors'])}; {e['capacity']}")
        if len(e['passengers']) + len(e['requests'])==e['capacity']:
            print(f"elevator {e['name']} is full")
        else:
            return e['name']

    return sim_building['elevators'][0]['name']


def main():
    parser = ArgumentParser()
    parser.add_argument("-f","--floors",help="enter number of floors in building",type=int)
    parser.add_argument("-e","--elevators",help="enter number of elevators in building",type=int)
    parser.add_argument("-c","--capacity",help="enter elevator capacity",type=int)
    # parser.add_argument("-s","--psgrs",help="number of passengers to model in simulation")
    args = parser.parse_args()
    sim_file_name = "simulation_list.json"
    results_file_name = "results_elevator.csv"
    passenger_stats_filename = "passenger_stats.csv"
    active_passengers = 0

    sim_building = create_building(args.floors, args.elevators, args.capacity)

    with open(sim_file_name, 'r') as sim_file:
        sim_list = json.load(sim_file)

    for t in range(12):
        print(f"starting time {str(t)} iteration")
        remaining_requests = len([p for p in sim_list if p['time'] > t])
        print(f"remaining requests: {remaining_requests}")

        # first, move elevator if it has passengers or requests
        # should be no movement at time zero since no passengers or requests yet
        for e in sim_building['elevators']:
            # print(f"elevator {e['name']} was on floor {e['curr_floor']}")
            print(f"""elevator {e['name']} has {len(e['passengers'])} passengers and {len(e['requests'])} requests, was on floor {e['curr_floor']}""")
            if len(e['passengers'])==0 and len(e['requests'])==0:
                print(f"elevator {e['name']} is still on floor {e['curr_floor']}")
            else:
                e['curr_floor'] += e['curr_direction']
                print(f"elevator {e['name']} is now on floor {e['curr_floor']}")

        # second, elevators unload and then load passengers based on current floor
            print(f"updating elevator {e['name']} at time {str(t)}")
            
            # unload first
            if len(e['passengers']):
                print(f"unloading riders for elevator {e['name']}")
                for p in e['passengers']:
                    if p['dest'] == e['curr_floor']:
                        unload_passenger(e,p)
                        active_passengers+=-1
                        p['end_time'] = t
                        with open(passenger_stats_filename,'a') as passenger_stats_file:
                            passenger_stats_file.write(f"{p['id']},{p['source']},{p['dest']},{p['start_time'] - p['request_time']},{p['end_time'] - p['start_time']}\n")
            else:
                print(f"elevator {e['name']} has no current passengers to unload")
            
        # third, new passengers for current time period make requests
        # and get assigned an elevator
        new_passengers = [p for p in sim_list if p['time']==t]

        if len(new_passengers):
            print(f"{len(new_passengers)} new passengers at time {str(t)}")
            for p in new_passengers:
                p['status'] = "waiting"
                p['request_time'] = t
                assigned_elevator_name = get_best_elevator(sim_building, p)
                for e in sim_building['elevators']:
                    if assigned_elevator_name==e['name']:
                        add_request(e,p)
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
                print(f"elevator {e['name']} has no current requests")

            # set direction for elevator for next tick of time, based on
            # requests and elevators
            if len(e['target_floors']):
                if min(e['target_floors']) > e['curr_floor']:
                    e['curr_direction'] = 1
                    print(f"direction is up; next stop: {min(e['target_floors'])}")
                elif max(e['target_floors']) < e['curr_floor']:
                    e['curr_direction'] = -1
                    print(f"direction is down; next stop: {max(e['target_floors'])}")

            print(f"elevator {e['name']} has {len(e['requests'])} requests and {len(e['passengers'])} riders")

            with open(results_file_name, 'a') as result_file:
                result_file.write(f"{t},{e['name']},{e['curr_floor']},{e['curr_direction']},{len(e['passengers'])},{len(e['requests'])},{e['target_floors']}\n")
        
        print(f"end of time {t}; active passengers: {active_passengers}")
        # stop simulation when no more active passengers and no future requests in sim file
        if active_passengers==0 and remaining_requests==0:
            print(f"simulation stopped; no new active passengers and no upcoming requests")
            break
    
    print("simulation complete")

if __name__ == "__main__":
    main()