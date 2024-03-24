import time
from queue import Queue


class BacktrackingAlgorithm:
    def __init__(self, maze_data, start_position, end_position, visualization_function, lock):
        self.maze_data = maze_data.copy()
        self.start_position = start_position
        self.end_position = end_position
        self.queue = Queue()
        self.visualization_function = visualization_function
        self.lock = lock

    def is_valid_move(self, row, col):
        rows, cols = self.maze_data.shape
        return 0 <= row < rows and 0 <= col < cols and self.maze_data[row, col] in {0, 2, -1}

    def run(self, canvas, label):
        startCas=time.time()
        path = [self.start_position]
        visited = set()
        visited.add(self.start_position)

        while path[-1] != self.end_position:
            row, col = path[-1]

            if (row, col) == self.end_position:
                return path

            if not self.is_valid_move(row, col):
                path.pop()
                continue

            self.maze_data[row, col] = 2

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            move_found = False

            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if self.is_valid_move(next_row, next_col) and (next_row, next_col) not in visited:
                    path.append((next_row, next_col))
                    visited.add((next_row, next_col))
                    move_found = True
                    break

            if not move_found:
                path.pop()

            self.visualization_function(self.maze_data, path, (row, col), canvas=canvas, algorithm_name="Backtracking",
                                        label=label)

        self.visualization_function(self.maze_data, path, None, canvas=canvas, algorithm_name="Backtracking", label=label)
        print("Backtracking:", round(time.time()-startCas,2), "sekund")
        return None

