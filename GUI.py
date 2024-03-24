import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import cv2
import threading
import numpy as np

from Astar import AStarAlgorithm
from Backtracking import BacktrackingAlgorithm
from Wavefront import WavefrontAlgorithm

def load_maze_from_image(image_path):
    maze_image = cv2.imread(image_path)
    maze_grayscale = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(maze_grayscale, 128, 255, cv2.THRESH_BINARY_INV)

    maze_data = (binary_image / 255).astype(int)
    return maze_data


def find_start_and_end(maze):
    start_col = 0
    start_row = np.argmax(maze[:, start_col] == 0)

    end_col = maze.shape[1] - 1
    end_row = np.argmax(maze[:, end_col] == 0)

    return (start_row, start_col), (end_row, end_col)


class AlgorithmThread(Thread):
    def __init__(self, algorithm, canvas, gui, label):
        super().__init__()
        self.algorithm = algorithm
        self.canvas = canvas
        self.gui = gui
        self.label = label

    def run(self):
        path = self.algorithm.run(canvas=self.canvas, label=self.label)


class AlgorithmVisualizer(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Algorithm Visualizer")

        maze_data = load_maze_from_image("maze/maze1.png")
        start_position, end_position = find_start_and_end(maze_data)

        self.lock = threading.Lock()

        self.astar_canvas, self.astar_label = self.create_canvas("A*")
        self.wavefront_canvas, self.wavefront_label = self.create_canvas("Wavefront")
        self.backtracking_canvas, self.backtracking_label = self.create_canvas("Backtracking")

        self.astar_algorithm = None
        self.wavefront_algorithm = None
        self.backtracking_algorithm = None


        self.astar_algorithm = AStarAlgorithm(maze_data, start_position, end_position, self.visualize_maze, self.lock)
        self.wavefront_algorithm = WavefrontAlgorithm(maze_data, start_position, end_position, self.visualize_maze,
                                                      self.lock)
        self.backtracking_algorithm = BacktrackingAlgorithm(maze_data, start_position, end_position,
                                                            self.visualize_maze, self.lock)

        self.astar_thread = AlgorithmThread(self.astar_algorithm, self.astar_canvas, self, self.astar_label)
        self.wavefront_thread = AlgorithmThread(self.wavefront_algorithm, self.wavefront_canvas, self,
                                                self.wavefront_label)
        self.backtracking_thread = AlgorithmThread(self.backtracking_algorithm, self.backtracking_canvas, self,
                                                   self.backtracking_label)

        self.astar_thread.start()
        self.wavefront_thread.start()
        self.backtracking_thread.start()


    def create_canvas(self, algorithm_name):
        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        label = tk.Label(frame, text=algorithm_name, font=("Helvetica", 20, "bold"))
        label.pack(side=tk.TOP)

        canvas = tk.Canvas(frame, width=450, height=450)
        canvas.pack(side=tk.TOP)

        return canvas, label

    def visualize_maze(self, maze_data, path=[], current_node=None, visited_cells=None, canvas=None,
                       algorithm_name=None, delay=10, label=None):

        self.lock.acquire()

        label.config(text=algorithm_name, bg="white", padx=10, pady=5)


        maze_visualization = np.ones((maze_data.shape[0], maze_data.shape[1], 3), dtype=np.uint8) * 255


        maze_visualization[maze_data == 1] = [0, 0, 0]


        visited_cells = set() if visited_cells is None else visited_cells

        for visited_cell in visited_cells:
            if isinstance(visited_cell, self.astar_algorithm.Node):
                row, col = visited_cell.row, visited_cell.col
                maze_visualization[row, col] = [0, 0, 255]
            else:
                row, col = visited_cell
                maze_visualization[row, col] = [0, 0, 255]


        for position in path:
            row, col = position
            maze_visualization[row, col] = [255, 0, 0]


        if current_node:
            if isinstance(current_node, self.astar_algorithm.Node):
                row, col = current_node.row, current_node.col
                maze_visualization[row, col] = [0, 255, 0]
            elif isinstance(current_node, tuple) and len(current_node) == 2:
                row, col = current_node
                maze_visualization[row, col] = [0, 255, 0]


        self.lock.release()


        self.after(delay, lambda: self.update_canvas(canvas, maze_visualization))

    def update_canvas(self, canvas, maze_visualization):

        resized_maze_visualization = cv2.resize(maze_visualization, (450, 450), interpolation=cv2.INTER_NEAREST)


        canvas.image = ImageTk.PhotoImage(image=Image.fromarray(resized_maze_visualization))
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)


if __name__ == "__main__":
    app = AlgorithmVisualizer()
    app.mainloop()
