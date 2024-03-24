import numpy as np
from queue import Queue
import time


class WavefrontAlgorithm:
    def __init__(self, maze_data, start_position, end_position, visualization_function, lock):
        self.maze_data = maze_data.copy()
        self.start_position = start_position
        self.end_position = end_position
        self.rows, self.cols = self.maze_data.shape
        self.wave_matrix = None
        self.visited_cells = set()
        self.visualization_function = visualization_function
        self.lock = lock

    def reconstruct_path(self, end_position):
        path = []
        current_position = end_position
        self.wave_matrix[end_position] = np.max(self.wave_matrix) + 1

        while self.wave_matrix[current_position[0], current_position[1]] > 1:
            path.append(current_position)
            row, col = current_position

            neighbors = [(row + dr, col + dc) for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]]

            valid_neighbors = [
                (r, c) for r, c in neighbors if
                0 <= r < self.rows and 0 <= c < self.cols and self.wave_matrix[r, c] != 0
            ]

            if not valid_neighbors:
                break

            next_position = min(valid_neighbors, key=lambda pos: self.wave_matrix[pos[0], pos[1]])
            current_position = next_position

        path.append(current_position)
        return path

    def run(self, canvas, label):
        startCas= time.time()
        self.wave_matrix = np.zeros_like(self.maze_data, dtype=int)

        start_row, start_col = self.start_position
        end_row, end_col = self.end_position

        self.wave_matrix[start_row, start_col] = 1
        self.wave_matrix[end_row, end_col] = -1

        self.q = Queue()
        self.q.put((start_row, start_col))

        # jen kvůli 1. cyklu
        next_row, next_col = start_row, start_col
        self.visited_cells.add((start_row,start_col))

        end = False

        while not self.q.empty() and not end:
            row, col = self.q.get()

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row, next_col = row + dr, col + dc
                # podmínka rychlejšího ukončení
                if (next_row, next_col) == (end_row, end_col):
                    end = True
                    break

                if 0 <= next_row < self.rows and 0 <= next_col < self.cols and self.wave_matrix[
                    next_row, next_col] == 0  and self.maze_data[next_row, next_col] in {0,-1}:
                    self.wave_matrix[next_row, next_col] = self.wave_matrix[row, col] + 1
                    self.q.put((next_row, next_col))
                    self.visited_cells.add((next_row, next_col))
                    self.visualization_function(self.maze_data, [], (next_row, next_col),
                                                visited_cells=self.visited_cells,
                                                canvas=canvas, algorithm_name="Wavefront", label=label)

        final_path = self.reconstruct_path(self.end_position)

        self.wave_matrix[list(zip(*self.visited_cells))] = 0


        self.visualization_function(self.maze_data, final_path, None, None, canvas=canvas,
                                    algorithm_name="Wavefront", label=label)

        print("Wavefront:",round(time.time()-startCas,2), "sekund")
        return None