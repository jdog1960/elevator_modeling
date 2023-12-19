import os
from sim_list_builder import build_simulation_list
import simulation_runner
from elevator_analyser import analyse_elevator_stats

def main():

    floors = 20
    elevators = 4
    capacity = 8
    passengers = 100
    time = 25
    
    sim_file_name = build_simulation_list(floors, passengers, time)
    
    # run same sim list through the three algorithms and generate results
    algorithm_list = ["simple_list","simple_random","same_dir"]

    for a in algorithm_list:
        # first run simulation for specified algorithm
        simulation_runner.main(floors,
                               elevators,
                               capacity,
                               a,
                               passengers,
                               time,
                               sim_file_name)
        
    # second, generate elevator summary stats
    file_list = [f for f in os.listdir("output") if "results_elevators" in f]
    first_in_line = True
    for f in file_list:
        analyse_elevator_stats(f, first_in_line)
        first_in_line = False



if __name__=="__main__":
    main()