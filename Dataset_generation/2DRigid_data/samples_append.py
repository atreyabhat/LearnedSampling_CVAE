import os
import glob
import csv

# Directory containing the map_ folders
base_directory = 'map_data/grid_map/controlled'

# Get all folders named map_x_omni
map_folders = glob.glob(os.path.join(base_directory, 'map_*_grid'))

# Output file for combined CSV contents within the 'map_data' folder
output_file = os.path.join(base_directory, 'Complete_training_data_grid_PRM_3.csv')

# Iterate through each map_x_omni folder, collect 'map_x_omni_samples.csv' files, and append their contents
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for folder in map_folders:
        map_number = folder.split('_')[-2]  # Extract the map number from the folder name

        # Find 'map_x_omni_samples.csv' files within each map_x_omni folder
        samples_files = glob.glob(os.path.join(folder, f'map_{map_number}_grid_samples.csv'))  # Adjust pattern as needed
        for file_name in samples_files:
            if os.path.isfile(file_name) and file_name.endswith('.csv'):
                with open(file_name, 'r') as infile:
                    reader = csv.reader(infile)
                    for row in reader:
                        # Insert the map number at the beginning of each row
                        row.insert(0, f'{map_number}')
                        writer.writerow(row)
