# Maze Solver Application

This application uses various algorithms to find a path through a maze. It includes implementations of the A* algorithm, Backtracking, and Wavefront to demonstrate their performance and pathfinding capabilities visually.

## Features
- Load mazes from image files.
- Automatically find the start and end points in a maze.
- Visualize the progress of each algorithm in real-time.
- Concurrent algorithm execution using threading.

## Algorithms
- **A***: Implemented in `Astar.py`, this algorithm uses heuristics to find the shortest path through the maze.
- **Backtracking**: Found in `Backtracking.py`, it explores the maze using depth-first search to backtrack when necessary.
- **Wavefront**: Described in `Wavefront.py`, it propagates a wave from the start to the end point, effectively flooding the maze to find a path.

## Visualization
Built with `tkinter`, the application provides a separate canvas for each algorithm, allowing the user to compare their strategies and performance visually. The visual feedback includes the representation of visited nodes and the current path.

## Getting Started
To run the application, execute `GUI.py` which initializes the GUI and starts the maze-solving process.

Make sure you have the following dependencies installed:
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow (PIL fork)

## Usage
- Place your maze image in the maze folder.
- Ensure that the start and end points are located at the leftmost and rightmost points, respectively.
- Run the `GUI.py` script to start the application and view the algorithms in action.

## Acknowledgements
- This project utilizes [OpenCV](https://opencv.org/) for image processing.
- GUI is powered by [Tkinter](https://docs.python.org/3/library/tkinter.html).
- Pathfinding algorithms are the core of this application, and their performance can be visually compared.
