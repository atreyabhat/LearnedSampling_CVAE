import numpy as np
import random
import os
from robot import OmnidirectionalRobot
from map_2d import Map2D

num_maps = 100
start = 1
num_configs = 60
map_d = 50
gap_d = 5
obs_d = 5
magic_numx = 45
magic_numy = 45
map_count = 0


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.linalg.norm(np.array(point1[:2]) - np.array(point2[:2]))


def generate_valid_configurations(num_configs, gap1, gap2):
    valid_configs = []
    count = 0
    while count < num_configs:
        # print("Generating configuration " + str(count) + " of " + str(num_configs))

        gap1xmin, gap1ymin, gap1xmax, gap1ymax = gap1
        gap2xmin, gap2ymin, gap2xmax, gap2ymax = gap2
        startoffset = 5
        goaloffset = 5

        # Generate random start and goal points
        while True:
            start = np.round(
                np.random.uniform(
                    low=(gap1xmin - startoffset, gap1ymin - startoffset, -np.pi),
                    high=(gap1xmax + startoffset, gap1ymax + startoffset, np.pi),
                ),
                1,
            )
            start[0:2] = start[0:2].astype(int)  # Round the x and y coordinates to integers

            goal = np.round(
                np.random.uniform(
                    low=(gap2xmin - goaloffset, gap2ymin - goaloffset, -np.pi),
                    high=(gap2xmax + goaloffset, gap2ymax + goaloffset, np.pi),
                ),
                1,
            )
            goal[0:2] = goal[0:2].astype(int)  # Round the x and y coordinates to integers

            # Calculate distance between start and goal
            distance = calculate_distance(start, goal)

            if distance >= 20:
                robot = OmnidirectionalRobot(width=1.5, height=3)
                collision1 = robot.check_collision_config(
                    start, map_2d.corners, map_2d.obstacles, map_2d.obstacle_edges
                )
                collision2 = robot.check_collision_config(
                    goal, map_2d.corners, map_2d.obstacles, map_2d.obstacle_edges
                )

                if not collision1 and not collision2:
                    valid_configs.append(np.concatenate((start, goal)))
                    count += 1
                    break

    return valid_configs


for i in range(start, num_maps + start):

    for _ in range(0,100):

        r1_ax = 0
        r1_ay = random.randint(gap_d, magic_numy)
        g1_ax = random.randint(gap_d, magic_numx)
        g1_ay = r1_ay
        R11 = [r1_ax, r1_ay, g1_ax, g1_ay, g1_ax, g1_ay + gap_d, r1_ax, r1_ay + obs_d]
        R12 = [
            g1_ax + gap_d,
            g1_ay,
            map_d,
            g1_ay,
            map_d,
            g1_ay + obs_d,
            g1_ax + gap_d,
            g1_ay + obs_d,
        ]

        gap1 = [g1_ax, g1_ay, g1_ax + gap_d, g1_ay + obs_d]

        r2_ax = random.randint(gap_d, magic_numx)
        r2_ay = 0
        g2_ax = r2_ax
        g2_ay = random.randint(gap_d, magic_numy)
        R21 = [r2_ax, 0, r2_ax + obs_d, 0, r2_ax + obs_d, g2_ay, g2_ax, g2_ay]
        R22 = [
            r2_ax + obs_d,
            map_d,
            r2_ax,
            map_d,
            g2_ax,
            g2_ay + gap_d,
            g2_ax + obs_d,
            g2_ay + gap_d,
        ]

        gap2 = [g2_ax, g2_ay, g2_ax + obs_d, g2_ay + gap_d]

        if calculate_distance([g1_ax,g1_ay],[g2_ax,g2_ay])<20:
            continue
        else:
            break

    R = [R11, R12, R21, R22]
    map_x = f"map_{i}_grid"  # Map name

    data_path = os.path.join(os.getcwd(), "map_data/grid_map/controlled")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    map_folder = os.path.join(data_path, map_x)
    if not os.path.exists(map_folder):
        os.makedirs(map_folder)

    map_file = os.path.join(map_folder, f"{map_x}.csv")
    print("Generating Configurations for Map " + str(i))
    with open(map_file, "w") as file:
        file.write("map shape,50,50\n")
        for obstacle in R:
            file.write(",".join(map(str, obstacle)) + "\n")

    # Load map inside the loop
    map_2d = Map2D(map_file)
    valid_configurations = generate_valid_configurations(num_configs, gap1, gap2)

    config_file = os.path.join(map_folder, f"{map_x}_configs.csv")
    with open(config_file, "w") as file:
        for config in valid_configurations:
            line = ",".join(map(str, config)) + "\n"
            file.write(line)
