# Drawings will be made with matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

class GridGenerator:
    def __init__(self, grid_info):
        """
        'grid_info' must have the following structure
        grid_info = {
            "row": int,
            "column": int,
            "edges": list,
            'start': list,
            'target': list,
        }
        """
        self.row = grid_info["row"]
        self.column = grid_info["column"]
        self.edges = grid_info["edges"]
        self.start = grid_info["start"]
        self.target = grid_info["target"]
    
    @staticmethod
    def generate_edges(edge_num, row, column):
        """
        Return 'edge_num' edges for a 'row' * 'column' grid
        """
        vertex_num = 2 * edge_num
        x = np.random.randint(1, row + 1, vertex_num).tolist()
        y = np.random.randint(1, column + 1, vertex_num).tolist()
        edges = [
            [[x[index], y[index]], [x[index + 1], y[index + 1]]] 
            for index in range(0, vertex_num, 2)
        ]
        return edges
    
    def draw(self):
        """
        Show the grid
        """
        x = np.linspace(1, self.row, self.row)
        y = np.linspace(1, self.column, self.column)
        x_grid, y_grid = np.meshgrid(x, y)

        plt.plot(x_grid, y_grid, marker='o', color='k', linestyle='none', markersize=0.2)
        plt.plot(self.start[0], self.start[1], marker='o', color='r', linestyle='none', markersize=1)
        plt.plot(self.target[0], self.target[1], marker='o', color='r', linestyle='none', markersize=1)
        for edge in self.edges:
            plt.plot(
                [edge[0][0], edge[1][0]],
                [edge[0][1], edge[1][1]],
                color='k',
                linewidth=0.2
            )

        plt.axis('scaled')
        plt.show()

    def save(self, path):
        """
        Save image in specified path
        """
        fig, ax = plt.subplots(1, 1)
        x = np.linspace(1, self.row, self.row)
        y = np.linspace(1, self.column, self.column)
        x_grid, y_grid = np.meshgrid(x, y)

        ax.plot(x_grid, y_grid, marker='o', color='k', linestyle='none', markersize=0.2)
        ax.plot(self.start[0], self.start[1], marker='o', color='r', linestyle='none', markersize=1)
        ax.plot(self.target[0], self.target[1], marker='o', color='r', linestyle='none', markersize=1)
        for edge in self.edges:
            ax.plot(
                [edge[0][0], edge[1][0]],
                [edge[0][1], edge[1][1]],
                color='k',
                linewidth=0.2
            )

        ax.axis('scaled')
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)

    def __repr__(self):
        string = f"Grid information:\n" +\
        f"Size: {self.row}*{self.column}\n" +\
        f"Number of edges: {len(self.edges)}\n" +\
        f"Start: {self.start}\n" +\
        f"Target: {self.target}"
        return string
    
# Instance for generating a grid
# row, col = 10, 10
# path = Path(__file__).parent/"Samples"/"Size10"/"sample1.json"
# edge_num = np.random.randint(min(row, col) / 2 + 1)
# edges = GridGenerator.generate_edges(edge_num, row, col)
# start = np.random.randint(1, [row + 1, col + 1]).tolist()
# target = np.random.randint(1, [row + 1, col + 1]).tolist()
# grid_info = {
#     "row": row,
#     "column": col,
#     "edges": edges,
#     "start": start,
#     "target": target
# }
# with open(path, "w") as f:
#     json.dump(grid_info, f, indent=1)


# Recreate samples
# for size in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
#     path = Path(__file__).parent/"Samples"
#     for index in range(1, 11):
#         edge_num = np.random.randint(size / 2 + 1)
#         edges = GridGenerator.generate_edges(edge_num, size, size)
#         start = np.random.randint(1, [size + 1, size + 1]).tolist()
#         target = np.random.randint(1, [size + 1, size + 1]).tolist()
#         grid_info = {
#             "row": size,
#             "column": size,
#             "edges": edges,
#             "start": start,
#             "target": target
#         }
#         new_path = path/f"Size{size}"/f"sample{index}.json"
#         with open(new_path, "w") as f:
#             json.dump(grid_info, f, indent=1)

# Save plots as .png images
# for size in [10*i for i in range(1, 11)]:
#     for index in range(1, 11):
#         grid_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"
#         save_path = Path(__file__).parent/"Image"/f"Size{size}"/f"sample{index}.png"
#         with open(grid_path, "r") as f:
#             grid_info = json.load(f)

#         A = GridGenerator(grid_info)
#         A.save(save_path)