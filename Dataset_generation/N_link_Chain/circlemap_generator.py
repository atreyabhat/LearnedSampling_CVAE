import numpy as np
import random
from robot import KinematicChain, OmnidirectionalRobot
import os
from map_2d import Map2D
from planner import Planner
from map_2d import Map2D



###############################################################################################
map_x = 'map_'  # Change the map version here

# Define circle centers and radii
#circle_centers = [(15, 10), (30, 15),(10, 40),(40,30),(25,30),(10,15)]
#circle_radii = [4, 5, 8, 5, 4]


#number of start,goal configurations
num_configs = 60
num_links = 4
arm_length = 8
##############################################################################################


def generate_valid_configurations(num_configs, circle_centers, circle_radii):
    valid_configs = []
    count = 0
    print("Generating " + str(num_configs) + " configurations ...")
    while count < num_configs:
        
        base = np.round(np.random.uniform(low=(0, 0), high=(50, 50)), 1)

        start = np.round(np.random.uniform(low=(-np.pi, -np.pi, -np.pi, -np.pi), high=(np.pi, np.pi, np.pi, np.pi)), 1)
        goal = np.round(np.random.uniform(low=(-np.pi, -np.pi, -np.pi, -np.pi), high=(np.pi, np.pi, np.pi, np.pi)), 1)

        robot = KinematicChain(link_lengths=[arm_length,arm_length,arm_length,arm_length], base=base)

        collision1 = robot.check_collision_config(start,map_2d.corners,map_2d.obstacles,map_2d.obstacle_edges)
        collision2 = robot.check_collision_config(goal,map_2d.corners,map_2d.obstacles,map_2d.obstacle_edges)


        if not collision1 and not collision2:
            valid_configs.append(np.concatenate((base, start, goal)))
            count += 1

    print("Done!")
    return valid_configs

def generate_circle(center, radius, num_vertices=20):
    angles = np.linspace(0, 2*np.pi, num_vertices)
    circle_verts = []
    for angle in angles:
        x = round(center[0] + radius * np.cos(angle), 1)
        y = round(center[1] + radius * np.sin(angle), 1)
        circle_verts.extend([x, y])
    return circle_verts

def distance(point1, point2):
        return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def generate_points(num_points, map_size, min_distance):
    points = []

    while len(points) < num_points:
        x = np.random.randint(5, map_size[0]-5)
        y = np.random.randint(5, map_size[1]-5)
        new_point = (x, y)

        if all(distance(new_point, existing_point) >= min_distance for existing_point in points):
            points.append(new_point)
            print(new_point)

    return points


if __name__ == "__main__":


    # Set parameters
    num_points = 5
    map_size = (50, 50)
    min_distance = 15

    for i in range(50):

        map_x = f'map_{i}_nlink'  # Map name

        # Generate points
        circle_centers = generate_points(num_points, map_size, min_distance)
        circle_radii = np.random.uniform(5, 7, 5)

        data_path = os.path.join(os.getcwd(), 'map_data/n_link') 
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        map_folder = os.path.join(data_path, map_x)
        if not os.path.exists(map_folder):
            os.makedirs(map_folder)

        # Generate and save map
        map_file = os.path.join(map_folder, f'{map_x}.csv')
        print("Generating Map file ...")
        with open(map_file, 'w') as file:
            file.write('map shape,50,50\n')
            for center, radius in zip(circle_centers, circle_radii):
                circle_vertices = generate_circle(center, radius)
                line = ','.join(map(str, circle_vertices)) + '\n'
                file.write(line)

        # Load map
        map_2d = Map2D(map_file)    
        #link_lengths = np.full(shape=(num_links,1), fill_value=arm_length)
        valid_configurations = generate_valid_configurations(num_configs, circle_centers, circle_radii)

        # Save configurations to CSV
        config_file = os.path.join(map_folder, f'{map_x}_configs.csv')
        with open(config_file, 'w') as file:
            for config in valid_configurations:
                line = ','.join(map(str, config)) + '\n'
                file.write(line)