# Conditional Variational Autoencoders (CVAE) for Motion Planning

This project explores CVAEs for optimizing pathfinding in various robotic scenarios, biasing sampling towards promising regions in the state space.

## Overview

Traditional random sampling might inefficiently explore state spaces, especially in constrained environments. CVAE learning targets this issue by focusing sampling efforts where optimal paths are likely to exist.

## Results

### Point Robot Path Planning
- CVAE-generated samples for the point robot
  ![Point Robot CVAE Samples](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/2dac1bb7-d16a-44d2-9e08-8c04418a51ee | width=300)
- CVAE-planned path for the point robot
  ![Point Robot CVAE Path](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/9663d388-66c8-461d-8f51-c07e32e79744 | width=300)

### 2D Rigid Path Planning
- CVAE-generated path for a 2D rigid configuration
  ![2D Rigid Path with CVAE](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/d5baf64c-9557-4ed3-852a-bed909751379 | width=300)

### Omnidirectional Robot Execution Time Comparison
- Comparison of execution time for the omnidirectional robot
  ![Execution Time Comparison](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/02998174-4795-474e-91ea-5ed317a5ba21 | width=300)

## Limitations and Future Work

- Challenges observed with higher-dimensional robots like n-link chains.
- Issues with accurately representing joint angles for sampling in narrow passages.
- Future work aims to refine CVAE performance in higher-dimensional spaces and improve input data representation.

This repository provides an exploration into the efficacy of CVAE-based motion planning, highlighting its potential in optimizing pathfinding for 2D omnidirectional robots.

## Additional Libraries Needed

- **NetworkX**: Install using `pip install networkx`

## Motion Planning Scripts

- `map_2d.py`
- `planner.py`
- `robot.py`
- `PRM.py`
- `RRT.py`
- `sampling_method.py`
- `utils.py`

## Usage

Run `*.ipynb` to execute the main programs.
