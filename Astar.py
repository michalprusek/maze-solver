import time
from queue import PriorityQueue



class AStarAlgorithm:
    class Node:
        def __init__(self, row, col, parent=None, cost=0, estimated_cost=0):
            self.row = row
            self.col = col
            self.parent = parent
            self.cost = cost #g
            self.estimated_cost = estimated_cost #h
            self.total_cost = cost + estimated_cost #f=g+h

    def __init__(self, maze_data, start_position, end_position, visualization_function, lock):
        self.maze_data = maze_data.copy()
        self.start_position = start_position
        self.end_position = end_position
        self.rows, self.cols = self.maze_data.shape
        self.visualization_function = visualization_function
        self.lock = lock
        self.visited_cells = set()

    def is_valid_move(self, row, col):
        return self.rows > row >= 0 and self.maze_data[row, col] == 0 and 0 <= col < self.cols

    @staticmethod
    def manhattan_distance(node, goal):
        return abs(node.row - goal[0]) + abs(node.col - goal[1])

    def run(self, canvas, label):
        startCas = time.time()
        start_node = self.Node(self.start_position[0], self.start_position[1])
        self.end_node = self.Node(self.end_position[0], self.end_position[1])

        start_node.total_cost = 0 + self.manhattan_distance(self.Node(self.start_position[0], self.start_position[1]),
                                                        self.end_position)

        self.open_set = PriorityQueue()
        self.open_set.put((start_node.total_cost, id(start_node), start_node))

        # u nás visited_cells a closed_set splývají
        self.closed_set = set()
        self.visited_cells = set()

        while not self.open_set.empty():
            current_node = self.open_set.get()[2]
            self.visited_cells.add((current_node.row, current_node.col))
            self.closed_set.add((current_node.row, current_node.col))

            #kontrola nalezení cesty
            if (current_node.row, current_node.col) == (self.end_node.row, self.end_node.col):
                path = self.reconstruct_path(current_node)
                self.visualization_function(self.maze_data, path, None, None,
                                            canvas=canvas,
                                            algorithm_name="A*", label=label)
                break

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row, next_col = current_node.row + dr, current_node.col + dc
                if self.is_valid_move(next_row, next_col) and (next_row, next_col) not in self.closed_set:
                    g = current_node.cost + 1
                    h = self.manhattan_distance(self.Node(next_row, next_col), self.end_position)
                    next_node = self.Node(next_row, next_col, current_node, g, h)

                    if (next_node.row, next_node.col) not in self.visited_cells or next_node.total_cost < current_node.total_cost:
                        self.open_set.put((next_node.total_cost, id(next_node), next_node))
                        self.visualization_function(self.maze_data, [], (next_node.row, next_node.col),
                                                    self.visited_cells, canvas=canvas,
                                                    algorithm_name="A*", label=label)

        print("A*:", round(time.time()-startCas,2), "sekund")
        return None

    def reconstruct_path(self, current_node):
        path = []
        while current_node:
            path.append((current_node.row, current_node.col))
            current_node = current_node.parent
        return path