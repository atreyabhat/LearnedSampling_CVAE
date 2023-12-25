# CVAE for Motion Planning

This project explores Conditional Variational Autoencoders (CVAE) for motion planning in different scenarios. It aims to optimize pathfinding by biasing sampling towards successful demonstrations and promising regions in the state space.

We have extended the work present in (https://github.com/StanfordASL/LearnedSamplingDistributions)

We also explore dataset generation for the same, based on different maps, start goal configurations for Point, 2D Rigid and Kinematic chain types. 

## Overview

Traditional random sampling might inefficiently explore state spaces, especially in constrained environments. CVAE learning targets this issue by focusing sampling efforts where optimal paths are likely to exist.

## Results

The CVAE implementation showcases enhanced success rates and convergence across diverse planning scenarios, notably improving pathfinding efficiency compared to traditional sampling methods.

![Point Robot CVAE Samples](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/2dac1bb7-d16a-44d2-9e08-8c04418a51ee)
![Point robot CVAE Path planned](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/9663d388-66c8-461d-8f51-c07e32e79744)
![2D Rigid path with CVAE](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/d5baf64c-9557-4ed3-852a-bed909751379)

![Comparison of Execution Time for Omnidirectional Robot](https://github.com/atreyabhat/LearnedSampling_CVAE/assets/39030188/02998174-4795-474e-91ea-5ed317a5ba21)

## Limitations and Future Work

- Challenges observed with higher-dimensional robots like n-link chains.
- Issues with accurately representing joint angles for sampling in narrow passages.
- Future work aims to refine CVAE performance in higher-dimensional spaces and improve input data representation.

This repository provides an exploration into the efficacy of CVAE-based motion planning, highlighting its potential in optimizing pathfinding for 2D omnidirectional robots.

## Additional Libraries Needed

- **NetworkX**: Install using `pip install networkx`

## Motion Planning Scripts

1. `map_2d.py`: Reads and initializes the obstacles and map size.
2. `planner.py`: Initializes the sampling method and visualizes the solution.
3. `robot.py`: Initializes the robot and corresponding parameters.
4. `PRM.py`: Used for probabilistic roadmaps to find a solution.
5. `RRT.py`: Used for rapidly exploring random trees to find a solution.
6. `sampling_method.py`: Parent class for PRM and RRT.
7. `utils.py`: Utilities script.

## Usage

Run `*.ipynb` to execute the main programs.
