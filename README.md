# Elevator Modeling System for Evaluation of Optimization Algorithms
Goal:  simulate operation of elevators in a building based on a feed of passenger requests and calculate performance in order to test algorithms for testing the best elevator for a request

## Items that support this goal
- Python code to simulate the operation of elevators in a building over a period of time
- JSON file that feeds passenger requests for an elevator
  - passenger's starting floor
  - passenger's target floor
- csv files generated with details from simulation:
  - elevator status at every point of time in the simulation
  - passenger trip statistics once his/her trip is complete
- Python code that inspects generated csv files and calculates statistics that
  support analysis of different algorithms for choosing the best elevator

## Simulation Details
- Time is represented by an integer that is incremented for each "tick" of the simulator's "clock"
- The building is represented by a dictionary that contains core elements:
  - number of floors
  - a list of elevators
- An elevator is represented as a dictionary that contains its elements:
  - a unique name
  - capacity
  - current direction
  - current floor
  - a list of passengers riding the elevator
  - a list of passengers who have requested the elevator
  - a list of the target floors for the elevator (for riders and requestors)
- A passenger is represented as a dictionary that contains its elements:
  - a unique id
  - the floor from which the passenger is requesting an elevator
  - the target floor, to which the passenger intends to get off
  - the time at which the passenger requests an elevator
  - the time at which the passenger boards an elevator
  - the time at which the passenger gets off the elevator

## How to Run The Simulator
1. Run the simulator using command line with the file "simulation_runner.py" with the following required switches
    - To set the number of floors use the switch "-f" or "--floors" followed by an integer
    - To set the number of elevators use the switch "-e" or "--elevators" followed by an integer
    - To set the capacity of an elevator use the switch "-c" or "--capacity" followed by an integer
    - To set the elevator request algorithm use the switch "-a" or "--algorithm" followed by a valid algorithm name
        - "simple_list":
            - pick the first elevator in the list that is not full at the passenger's "pick up" floor
            - if all elevators are full, pick the first elevator in the list
        - "simple_random":
            - shuffle the elevator list
            - pick the first elevator in the list that is not full at the passenger's "pick up" floor
            - if all elevators are full, pick an elevator randomly from the list
        - "same_dir": 
            - reduce the elevator list to only those that are heading same direction as the passenger
            - reduce this list to only those elevators that are heading toward the passenger
            - sort the list of remaining elevators in order of closeness to the passenger's "pick up" floor
            - pick the first elevator in the list that is not full at the passenger's "pick up" floor
            - if no elevators can be found this way, get the elevator with the smallest number of demands
              - demands = requests + riders, represented by the length of an elevator's "target_floors" list
    - To set the number of passengers to model use the switch "-p" or "--passengers" followed by an integer
    - To set the range of time during which a passenger can request an elevator use the switch "-t" or  "--time" followed by an integer
   
3. When the simulation is complete, two files are created and can be analysed for performance:
    - **passenger_stats.csv**: details for each passenger's trip
    - **results_elevators.csv**: detailed log of each elevator's travel during the simulation
    - run the simulator (filename) to generate summary statistics in the following files
        - file a (TODO)
        - file b (TODO)
        - file c (TODO)

## Implementation Details: simulator
1. Based on arguments in the command line, the simulator configures the simulation
    - create a json file with a list of passenger requests
      - number of requests is based on the -p argument
      - time range for each request is based on the -t argument
    - create a building represented by a dictionary, with number of floors and a list of elevators
      - all elevators are initialized with current floor being 1 and direction being up (+1)
    - set the type of algorithm to be used for the matching of an elevator to each request
2. For each "tick" of time, represented by an incrementing integer, the simulator does the following:
    - **Update Elevator Location**: move the elevator to the next floor, based on its direction
        - if the elevator has no passengers and no requests, it stays where it is
    - **Unload Arrived Passengers**: based on each elevator's current floor, unload any passengers who have arrived at their target floor
    - **Check For New Passengers**: check the simulation_list file for any new passenger requests at the current time
    - **Assign Requests To Elevators**: if there are any new requests, assign the passenger to an elevator
        - algorithm is used to pick the best elevator
        - the passenger is added as a "request" to the elevator
    - **Load New Passengers**: load passengers on their requested elevator if applicable
        - elevator has a request for a passenger whose request floor ("source") is the current floor for that elevator
        - convert the passenger from a "request" to a "passenger"
            - passenger is removed from "requests" list and added to "passengers" list
            - passenger request floor ("source") is removed from the elevator's "targets" list
            - passenger destination floor ("dest") is added to the elevator's "targets" list