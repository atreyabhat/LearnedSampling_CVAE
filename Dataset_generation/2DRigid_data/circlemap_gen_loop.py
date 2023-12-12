import numpy as np
import random
from robot import KinematicChain, OmnidirectionalRobot
import os
from map_2d import Map2D
from planner import Planner
from map_2d import Map2D

num_maps = 2
num_configs = 5

def generate_valid_configurations(num_configs):
    valid_configs = []
    count = 0
    while count < num_configs:
        #print("Generating configuration " + str(count) + " of " + str(num_configs))

        # Generate random start and goal points
        while True:
            start = np.round(np.random.uniform(low=(10, 10, -np.pi), high=(40, 40, np.pi)), 1)
            start[0:2] = start[0:2].astype(int)  # Round the x and y coordinates to integers

            goal = np.round(np.random.uniform(low=(10, 10, -np.pi), high=(40, 40, np.pi)), 1)
            goal[0:2] = goal[0:2].astype(int)  # Round the x and y coordinates to integers

            # Calculate distance between start and goal
            distance = np.linalg.norm(start[:2] - goal[:2])

            if distance >= 15:
                robot = OmnidirectionalRobot(width=1.5, height=3)
                collision1 = robot.check_collision_config(start, map_2d.corners, map_2d.obstacles, map_2d.obstacle_edges)
                collision2 = robot.check_collision_config(goal, map_2d.corners, map_2d.obstacles, map_2d.obstacle_edges)

                if not collision1 and not collision2:
                    valid_configs.append(np.concatenate((start, goal)))
                    count += 1
                    break

    return valid_configs

def generate_circle(center, radius, num_vertices=20):
    angles = np.linspace(0, 2*np.pi, num_vertices)
    circle_verts = []
    for angle in angles:
        x = round(center[0] + radius * np.cos(angle), 1)
        y = round(center[1] + radius * np.sin(angle), 1)
        circle_verts.extend([x, y])
    return circle_verts

def move_circle_rand(position, max_distance):


    # Generate random movement within given constraints
    new_x = position[0] + random.uniform(-max_distance, max_distance)
    new_y = position[1] + random.uniform(-max_distance, max_distance)
    
    # Ensure movement stays within bounds
    new_x = max(min(new_x, 45), 0)  # Bound within x range 0-45
    new_y = max(min(new_y, 45), 0)  # Bound within y range 0-45
    
    return (new_x, new_y)

    
def move_circle_controlled(position):
    random_distance_horiz_vert = random.randint(5, 15)  # Random distance for horizontal and vertical movements

    if position == (10, 10):
        new_x = min(position[0] + random_distance_horiz_vert, 45)
        new_y = position[1]
    elif position == (40, 10):
        new_x = position[0]
        new_y = min(position[1] + random_distance_horiz_vert, 45)
    elif position == (40, 40):
        new_x = max(position[0] - random_distance_horiz_vert, 0)
        new_y = position[1]
    elif position == (10, 40):
        new_x = position[0]
        new_y = max(position[1] - random_distance_horiz_vert, 0)
    elif position == (20, 20):
        # Restrict movement only up (increase y position)
        new_x = position[0]
        new_y = min(position[1] + random_distance_horiz_vert, 45)
    elif position == (30, 30):
        # Restrict movement only down (decrease y position)
        new_x = position[0]
        new_y = max(position[1] - random_distance_horiz_vert, 0)
    else:
        new_x = position[0]
        new_y = position[1]
    
    return (new_x, new_y)



for i in range(1, num_maps + 1):
    map_x = f'map_{i}_omni'  # Map name

    # Fixed positions for circles in map1
    fixed_positions = [(10, 10), (40, 10), (40, 40), (10, 40), (20, 20), (30, 30), (25,25) , (30,40)]
    circle_radii = [6, 5, 5, 5, 4, 4, 3, 3] 
    #circle_radii = [random.uniform(3, 5) for _ in range(7)]
    

    for j in range(len(fixed_positions)):
        fixed_positions[j] = move_circle_controlled(fixed_positions[j])
    circle_centers = fixed_positions.copy()

    # # Move the first 4 circles within a maximum distance of 5 units
    # for i in range(4):
    #     circle_centers[i] = move_circle(circle_centers[i], 4, rand=rand)

    # # Move the last 2 circles sideways to left and right, with a maximum distance of 10 units
    # circle_centers[4] = move_circle(circle_centers[4], 8, rand=rand)
    # circle_centers[5] = move_circle(circle_centers[5], 8, rand=rand)

    data_path = os.path.join(os.getcwd(), 'map_data/controlled_movement')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    map_folder = os.path.join(data_path, map_x)
    if not os.path.exists(map_folder):
        os.makedirs(map_folder)

    map_file = os.path.join(map_folder, f'{map_x}.csv')
    print("Generating Configurations for Map " + str(i))
    with open(map_file, 'w') as file:
        file.write('map shape,50,50\n')
        for center, radius in zip(circle_centers, circle_radii):
            circle_vertices = generate_circle(center, radius)
            line = ','.join(map(str, circle_vertices)) + '\n'
            file.write(line)

    # Load map inside the loop
    map_2d = Map2D(map_file)
    valid_configurations = generate_valid_configurations(num_configs)

    config_file = os.path.join(map_folder, f'{map_x}_configs.csv')
    with open(config_file, 'w') as file:
        for config in valid_configurations:
            line = ','.join(map(str, config)) + '\n'
            file.write(line)



 