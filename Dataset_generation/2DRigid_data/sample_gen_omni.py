import os
from map_2d import Map2D
from planner import Planner
from robot import KinematicChain,OmnidirectionalRobot
from PRM import PRM
import numpy as np
from RRT import RRT




##########################################################################################################

# Set the map version, arm length, and link lengths here
map_sl = '_grid'
sampler = "bridge"
#num of maps to sample
n = 150
start = 1
##########################################################################################################



for i in range(start,n+1):

    configurations = []

    # Set up folder paths
    map_x = 'map_' + str(i) + '_grid'
    data_path = os.path.join(os.getcwd(), 'map_data/grid_map/random')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    map_folder = os.path.join(data_path, map_x)
    if not os.path.exists(map_folder):
        print("Map " + map_x + " does not exist, Skipping ->> ")
        continue

    # Load configurations from the respective folder
    config_file = os.path.join(map_folder, f'{map_x}_configs.csv')
    with open(config_file, 'r') as file:
        next(file)  # Skip header
        for line in file:
            config = list(map(float, line.strip().split(',')))
            configurations.append(config)

    # Load the map
    map_file = os.path.join(map_folder, f'{map_x}.csv')
    map_2d = Map2D(map_file)
    method = PRM(sampling_method=sampler, n_configs=30, kdtree_d=30)
    #method =  RRT(sampling_method="RRT_star", n_configs=40, kdtree_d=10)

    # Load the occupancy grid map CSV
    occupancy_grid_file = os.path.join(map_folder, f'{map_x}.csv_occup.csv')
    occupancy_grid = []
    with open(occupancy_grid_file, 'r') as occupancy_file:
        for row in occupancy_file:
            occupancy_grid.append(row.strip())

    # Generate samples for each configuration
    samples_array = []
    count = 1
    path_found_count = 0

    for config in configurations:
        print("Map " + str(i) + " : Sampling for configuration " + str(count) + " of " + str(len(configurations)+1) + "...")
        robot = OmnidirectionalRobot(width=1.5, height=3)
        start = (config[0], config[1], config[2])
        goal = (config[3], config[4], config[5])
        planner = Planner(method, map_2d, robot)
        solution, samples = planner.plan(start, goal)
        concatenated_occupancy = ','.join(occupancy_grid)
        planner.visualize(make_video=False)

        # for PRM planners
        if solution and samples:
            
            for s in samples:
                s_round = [round(val, 2) for val in s]
                
                sample_str = ','.join(map(str, s_round)) + ',' + ','.join(map(str, start)) + ',' + ','.join(map(str, goal)) + ',' + concatenated_occupancy
                samples_array.append(sample_str)

            path_found_count+=1

        # for Search Based planners
        elif solution is not None:
            
            for s in solution[1:-1]:
                s_round = [round(val, 2) for val in s]
                
                sample_str = ','.join(map(str, s_round)) + ',' + ','.join(map(str, start)) + ',' + ','.join(map(str, goal)) + ',' + concatenated_occupancy
                samples_array.append(sample_str)

            path_found_count+=1
        else:
            continue

        count += 1

    print("Sampled for " + str(path_found_count) + " configurations")
    # Save samples to CSV
    samples_file = os.path.join(map_folder, f'{map_x}_samples.csv')

    with open(samples_file, mode='w') as file:
        file.write('\n'.join(samples_array))  # Write all samples in one line each



