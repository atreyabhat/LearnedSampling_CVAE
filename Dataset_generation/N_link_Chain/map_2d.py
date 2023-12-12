import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from utils import endpoints_to_edges
from PIL import Image
import os


class Map2D():
    """A 2D map class in the continuous space (x, y).
    The map has a rectangular shape and a list of obstacles.
    """
    def __init__(self, file_path):
        map_2d = self.load_map(file_path)
        # (x_lim, y_lim)
        self.shape = map_2d[0]
        # four corners of the map
        self.corners = map_2d[1]
        # list of obstacles
        self.obstacles = map_2d[2]
        # list of obstacle edges including map boundary
        self.obstacle_edges = map_2d[3]  

        self.save_path = file_path
        
        self.visualize_map()

    def load_map(self, file_path):
        """Load a map in the continuous space with shape (x_lim, y_lim), and
        each obstacle is defined as a list of points [(x1, y1), (x2, y2), ...]
        """
        # Map container
        shape = [0, 0]
        corners = []
        obstacles = []
        obstacle_edges = []

        # Load from the csv file
        # the first row is the map size
        # the rest of the rows are obstacle vertices
        with open(file_path, 'r') as map_file:
            reader = csv.reader(map_file)
            for i, row in enumerate(reader):

                # load the map size
                if i == 0:
                    shape[0] = float(row[1])
                    shape[1] = float(row[2])

                # load the obstacles
                else:
                    obstacle = []
                    # load (x, y) as obstacle vertices
                    for j in range(0, len(row), 2):
                        if row[j] == '' or row[j + 1] == '':
                            break
                        point = (float(row[j]), float(row[j + 1]))
                        obstacle.append(point)
                    obstacles.append(obstacle)

        # Set the map corners
        corners = [
            [0, 0], 
            [shape[0], 0],
            [shape[0], shape[1]], 
            [0, shape[1]]
        ]

        # Build the edges of obstacles
        # including obstacle edges and map boundary edges

        # a. map boundary edges
        corners = [
            (0, 0), 
            (shape[0], 0), 
            (shape[0], shape[1]), 
            (0, shape[1])
        ]
        boundary_edges = endpoints_to_edges(corners, closed=True)
        obstacle_edges.extend(boundary_edges)

        # b. convert obstacles to obstacle edges
        for obstacle in obstacles:
            each_edges = endpoints_to_edges(obstacle, closed=True)
            obstacle_edges.extend(each_edges)

        return shape, corners, obstacles, obstacle_edges



    def visualize_map(self, return_ax=False):
        """Visualize the map and save as PNG and Occupancy Grid CSV."""

        save_path = self.save_path  + '.png'  # Updated PNG file name
        occupancy_csv_path = self.save_path + '_occup.csv'  # Updated CSV file name
        
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        ax.set_xlim(0, self.shape[0])
        ax.set_ylim(0, self.shape[1])
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

        for obstacle in self.obstacles:
            polygon = Polygon(
                obstacle, closed=True, edgecolor='black', facecolor='black'
            )
            ax.add_patch(polygon)

        if return_ax:
            return ax, fig
        else:
            #plt.show()
            ax.axis('off')

            if save_path:
                fig.savefig(save_path, bbox_inches='tight', pad_inches=0)

            # Convert saved PNG to occupancy grid
            if save_path and occupancy_csv_path:
                img = Image.open(save_path).convert('L')  # Open saved PNG as grayscale
                
                # Calculate new size for occupancy grid (ensuring integer values)
                img = img.resize((int(self.shape[0]), int(self.shape[1])))  # Resize to map dimensions

                # Convert image to numpy array
                occupancy_grid = np.array(img) // 255  # Convert pixel values to 0 or 1

                # Save occupancy grid as CSV with concatenated rows
                with open(occupancy_csv_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in occupancy_grid:
                        writer.writerow(row)
