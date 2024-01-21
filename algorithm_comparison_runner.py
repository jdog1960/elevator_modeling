import os
from sim_list_builder import build_simulation_list
import simulation_runner
from elevator_analyser import analyse_elevator_stats
from passenger_analyser import analyse_passenger_stats

def main(sim_list_file_name:str=None):

    floors = 20
    elevators = 4
    capacity = 8
    passengers = 100
    time = 25

    sim_file_name = sim_list_file_name

    if not sim_file_name:
        sim_file_name = build_simulation_list(floors, passengers, time)
    
    # run same sim list through the three algorithms and generate results
    algorithm_list = [{'code':'sl','name':'simple_list'},
                       {'code':'sr','name':'simple_random'},
                       {'code':'sd','name':'same_dir'}]

    for a in algorithm_list:
        # first run simulation for specified algorithm
        simulation_runner.main(floors,
                               elevators,
                               capacity,
                               a['code'],
                               passengers,
                               sim_file_name)
        
    # second, generate elevator summary stats
    file_list = [f for f in os.listdir("output") if "results_elevators" in f]
    first_in_line = True
    for f in file_list:
        analyse_elevator_stats(f, first_in_line)
        first_in_line = False

    # third, generate passenger summary stats
    file_list = [f for f in os.listdir("output") if "passenger_stats" in f]
    first_in_line = True
    for f in file_list:
        analyse_passenger_stats(f, first_in_line)
        first_in_line = False


if __name__=="__main__":
    """option to skip creation of new sim list if testing changes"""
    sim_list_file_name = "/Users/jacksn/Programs/repos/elevator_modeling/input/simulation_list_2024_01_15_111338.json"
    main(sim_list_file_name)