import os
from map_2d import Map2D
from planner import Planner
from robot import KinematicChain
from PRM import PRM
import numpy as np
import csv

configurations = []

##########################################################################################################

# Set the map version, arm length, and link lengths here
arm_length = 8
link_lengths = [arm_length, arm_length, arm_length, arm_length]

# Set the map version, arm length, and link lengths here
map_sl = '_nlink'
sampler = "bridge"
#num of maps to sample
n = 50
start = 10

##########################################################################################################

for i in range(start, n + 1):
    configurations = []

    # Set up folder paths
    map_x = 'map_' + str(i) + '_nlink'
    data_path = os.path.join(os.getcwd(), 'map_data/n_link')
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
    method = PRM(sampling_method=sampler, n_configs=20, kdtree_d=20)
    # method =  RRT(sampling_method="RRT_star", n_configs=40, kdtree_d=10)

    # Load the occupancy grid map CSV
    occupancy_grid_file = os.path.join(map_folder, f'{map_x}.csv_occup.csv')
    occupancy_grid = []
    with open(occupancy_grid_file, 'r') as occupancy_file:
        for row in occupancy_file:
            occupancy_grid.append(row.strip())

    count = 1
    path_found_count = 0
    concatenated_occupancy = ','.join(occupancy_grid)
    samples_file = os.path.join(map_folder, f'{map_x}_samples.csv')

    with open(samples_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for config in configurations:

            print("Map " + str(i) + " : Sampling for configuration " + str(count) + " of " + str(
                len(configurations) + 1) + "...")
            robot = KinematicChain(link_lengths=link_lengths, base=[config[0], config[1]])
            start = (config[2], config[3], config[4], config[5])
            goal = (config[6], config[7], config[8], config[9])
            planner = Planner(method, map_2d, robot)
            solution, samples = planner.plan(start, goal)

            samples_array = []  # Initialize a new array for each configuration

            if solution:
                planner.visualize(make_video=False)

                for s in samples:
                    # Flatten 's' to remove nested arrays and convert to string
                    flattened_s = ','.join(map(str, np.array(np.round(s,5)).flatten()))
                    formatted_row = f"{flattened_s},{','.join(map(str, start))},{','.join(map(str, goal))},{','.join(map(str, concatenated_occupancy))}"
                    formatted_row = formatted_row.replace("'", "").replace('"', "").replace("[", "").replace("]", "").replace(",,,",",")
                    csv_writer.writerow(formatted_row.split(','))  # Write each 's' as separate values in different columns


                    #samples_array.append(concatenated_occupancy)
                

                path_found_count += 1

            count += 1

            # Save samples to CSV for each configuration
            csv_writer.writerow(samples_array)

        print("Sampled for " + str(path_found_count) + " configurations")

    

#    # Save samples in the required format with two decimal points
#     with open(samples_file, 'w') as file:
#         for i in range(0, len(samples_array), 4):
#             formatted_lines = []
#             for s in samples_array[i:i + 4]:
#                 if isinstance(s, list):
#                     formatted_line = ','.join(
#                         '{:.2f}'.format(round(coord, 2)) if isinstance(coord, float) else str(coord)
#                         for point in s for coord in point)
#                 else:
#                     formatted_line = s  # For the occupancy grid
#                 formatted_lines.append(formatted_line)
#             file.write(','.join(formatted_lines) + '\n')




