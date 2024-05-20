import matplotlib.pyplot as plt
import math
import os
import json
from pathlib import Path

def check_intersection(point1, point2, edge):
    """
    Check intersection of segment ['point1', 'point2'] with 'edge'
    """
    a1, b1, a2, b2 = edge[0][0], edge[0][1], edge[1][0], edge[1][1]
    x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
    """
    Solve the following system
    u*(a1 - a2) - v*(x1 - x2) = x2 - a2
    u*(b1 - b2) - v*(y1 - y2) = y2 - b2
    Condition of intersection: u, v in [0, 1]
    """
    d = (a2 - a1)*(y1 - y2) + (b1 - b2)*(x1 - x2)
    d1 = (a2 - x2)*(y1 - y2) + (y2 - b2)*(x1 - x2)
    d2 = (a1 - a2)*(y2 - b2) + (b2 - b1)*(x2 - a2)
    if d == 0:
        if d1 != 0 or d2 != 0: return False
        else:
            a12 = a1 - a2
            if a12 == 0:
                b12 = b1 - b2
                y1b2 = y1 - b2
                y2b1 = y2 - b1
                if b12 > 0:
                    return (y1b2 >= 0 and y2b1 <= 0)
                else: 
                    return (y1b2 <= 0 and y2b1 >= 0)
            else:
                x1a2 = x1 - a2
                x2a1 = x2 - a1
                if a12 > 0:
                    return (x1a2 >= 0 and x2a1 <= 0)
                else:
                    return (x1a2 <= 0 and x2a1 >= 0)
                
    else:
        cond_u = (all([d > 0, d1 >= 0, d1 - d <= 0]) or all([d < 0, d1 <= 0, d1 - d >= 0]))
        cond_v = (all([d > 0, d2 >= 0, d2 - d <= 0]) or all([d < 0, d2 <= 0, d2 - d >= 0]))
        return all([cond_u, cond_v])

# Example check
"""
point1, point2 = [4, 1], [2, 4]
edge = [[3, 4], [4, 6]]
print(check_intersection(point1, point2, edge))
plt.plot(
    [point1[0], point2[0]],
    [point1[1], point2[1]],
)
plt.plot(
    [edge[0][0], edge[1][0]],
    [edge[0][1], edge[1][1]],
)
plt.axis("scaled")
plt.show()
"""

# Generate slopes dictionary for grid
def reduce_tuple(iter):
    """
    Reduce the iterable (a, b)
    """
    a, b = iter[0], iter[1]
    d = math.gcd(a, b)
    return (int(a/d), int(b/d))

def get_slopes(current_col, current_row, row, col):
    """
    Return list of slopes for point ('i', 'j') in a
    'row' * 'col' grid. A slope is represented as an
    irreducible list [a, b], in the right-upward direction (i.e b > 0,
    or b = 0 and a > 0)
    """
    slope_set = set()
    if current_col < col:
        slope_set.add((1, 0))
    for row_index in range(current_row + 1, row + 1):
        for col_index in range(1, col + 1):
            slope_set.add(reduce_tuple((col_index - current_col, row_index - current_row)))
    return list(slope_set)

# Example for get_slopes
# print(get_slopes(1, 1, 4, 4))
# [(0, 1), (1, 2), (2, 1), (3, 1), (1, 1), (2, 3), (1, 0), (3, 2), (1, 3)]
# print(get_slopes(4, 4, 4, 4))
# []

# Get reach from a point
def get_furthest_reach(point, slope, row, col, edge_list):
    """
    Get furthest expansion from 'point' in the direction given by 'slope',
    in a 'row'*'col' grid with 'edge_list' as obstacles.
    """
    current_col, current_row = point[0], point[1]
    col_slope, row_slope = slope[0], slope[1]
    # Get maximum column reach
    if col_slope == 0: max_col_reach = col
    elif col_slope > 0: max_col_reach = int((col - current_col) / col_slope) + 1
    else: max_col_reach = int((current_col - 1) / (-col_slope)) + 1
    # Get maximum row reach
    if row_slope == 0: max_row_reach = row
    else: max_row_reach = int((row - current_row) / row_slope) + 1

    min_reach = 0
    max_reach = min(max_row_reach, max_col_reach)
    while max_reach - min_reach > 1:
        temp = min_reach
        new_reach = int((max_reach + min_reach) / 2)
        min_reach = new_reach
        test_point = [current_col + new_reach * col_slope, current_row + new_reach * row_slope]
        for edge in edge_list:
            if check_intersection(point, test_point, edge):
                max_reach = new_reach
                min_reach = temp
                break
    return min_reach

# Example for get_furthest_reach()
"""
point = [1, 1]
slope = [1, 1]
row, col = 6, 6
edge_list = [[[3, 4], [4, 6]], [[6, 1], [4, 4]]]
max_reach = get_furthest_reach(point, slope, row, col, edge_list)
# print(get_furthest_reach(point, slope, row, col, edge_list)) -> 2
for edge in edge_list:
    plt.plot(
        [edge[0][0], edge[1][0]],
        [edge[0][1], edge[1][1]],
        color='k',
        linewidth=0.2
    )
plt.plot(
    [point[0], point[0] + max_reach * slope[0]],
    [point[1], point[1] + max_reach * slope[1]],
    marker="o",
    color="b",
)
plt.show
"""

# point = [4, 3]
# slope = [0, 1]
# row, col = 4, 4
# edge_list = [[[1, 2], [3, 3]], [[4, 1], [4, 2]]]
# max_reach = get_furthest_reach(point, slope, row, col, edge_list)
# print(max_reach)

# Sort the edge_list, to speed up categorization
def sort_edge_list(edge_list):
    """
    Sort edge_list by length of edge, from longest to shortest, using
    taxicab distance
    """
    return sorted(
        edge_list, 
        key=lambda x: abs(x[0][0] - x[1][0]) + abs(x[0][1] - x[1][1]),
        reverse=True,
    )

# Example
# print(sort_edge_list([[[3, 4], [4, 6]], [[6, 1], [4, 4]]]))
# [[[6, 1], [4, 4]], [[3, 4], [4, 6]]]

# Convert grid coordinates to num, and vice versa
def coords_to_num(current_col, current_row, col):
    """
    Note: no row index needed
    """
    return col*(current_row - 1) + current_col

def num_to_coords(num, col):
    """
    Note: No row index needed
    """
    current_row = int(num / col) + 1
    current_col = num - col*(current_row - 1)
    return [current_col, current_row]

# Slopes generation for square grid
def generate_slopes_10_to_100():
    for size in [10*i for i in range(1, 11)]:
        slope_dict = dict()
        path = Path(__file__).parent/"Slopes"/f"Size{size}"
        for current_row in range (1, size + 1):
            for current_col in range (1, size + 1):
                slope_dict[f"{current_col}_{current_row}"] = get_slopes(
                    current_col, current_row, size, size,
                )
        with open(path, "w") as f:
            json.dump(slope_dict, f, indent=1)

# Sort edge_list for existing samples
def sort_edge_list_10_to_100():
    for size in [10*i for i in range(1, 11)]:
        for index in range(1, 11):
            grid_info = dict()
            read_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"
            with open(read_path, "r") as f_out:
                grid_info = json.load(f_out)
            edge_list = grid_info["edges"]
            sorted_edge_list = sort_edge_list(edge_list)
            edge_info = {
                "edges": sorted_edge_list
            }
            write_path = Path(__file__).parent/"Sorted_edge_list"/f"Size{size}"/f"sample{index}.json"
            with open(write_path, "w") as f_out:
                json.dump(edge_info, f_out, indent=1)

# Generate redundant nodes list, to be used later
def get_points_between(point1, point2):
    """
    Return list of all integral points between 'point1' and 'point2'
    """
    a1, b1, a2, b2 = point1[0], point1[1], point2[0], point2[1]
    a, b = a2 - a1, b2 - b1
    if b > 0 or (b == 0 and a > 0):
        d = math.gcd(a, b)
        i, j = int(a/d), int(b/d)
        return [[a1 + num * i, b1 + num * j] for num in range(0, d + 1)]
    else:
        a, b = -a, -b
        d = math.gcd(a, b)
        i, j = int(a/d), int(b/d)
        return [[a2 + num * i, b2 + num * j] for num in range(0, d + 1)]

# Examples
# print(get_points_between([1, 1], [3, 5]))
# [[1, 1], [2, 3], [3, 5]]
# print(get_points_between([4, 4], [1, 1]))
# [[1, 1], [2, 2], [3, 3], [4, 4]]

def generate_redundant_points_list_10_to_100():
    for size in [10*i for i in range(1, 11)]:
        for index in range(1, 11):
            edge_path = Path(__file__).parent/"Sorted_edge_list"/f"Size{size}"/f"sample{index}.json"
            with open(edge_path, "r") as f:
                edges = json.load(f)["edges"]
            redundant_point_set = set()
            for edge in edges:
                point1, point2 = edge[0], edge[1]
                redundant_points = get_points_between(point1, point2)
                for redundant_point in redundant_points:
                    redundant_point_set.add(tuple(redundant_point))
            redundant_point_list = list(redundant_point_set)
            dict = {
                "redundant_point_list": redundant_point_list
            }
            redundant_point_path = Path(__file__).parent/"Redundant_points_list"/f"Size{size}"/f"sample{index}.json"
            with open(redundant_point_path, "w") as f:
                json.dump(dict, f, indent=1)

# Generate nodes info
def is_empty_dict(dict):
    """
    Checks for empty dictionaries (values are empty lists)
    """
    return all(len(dict[key]) == 0 for key in dict.keys())

# To be run
# size = 40
# for index in range(1, 11):

#     nodes_info = {
#     f"{i}_{j}": {
#         "begin": [], 
#         "middle": [], 
#         "end": []
#     } 
#     for j in range(1, size + 1) for i in range(1, size + 1)
# }

#     slopes_path = Path(__file__).parent/"Slopes"/f"Size{size}"
#     with open(slopes_path, "r") as f:
#         node_slopes = json.load(f)

#     grid_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"
#     with open(grid_path, "r") as f:
#         grid_info = json.load(f)

#     edge_path = Path(__file__).parent/"Sorted_edge_list"/f"Size{size}"/f"sample{index}.json"
#     with open(edge_path, "r") as f:
#         edges = json.load(f)["edges"]

# # When you have the redundant point list, change this
#     redundant_points_path = Path(__file__).parent/"Redundant_points_list"/f"Size{size}"/f"sample{index}.json"
#     with open(redundant_points_path, "r") as f:
#         redundant_points = json.load(f)["redundant_point_list"]

#     nodes_list = [[i, j] for j in range(1, size + 1) for i in range(1, size + 1)]
#     for point in redundant_points:
#         nodes_list.remove(point)

#     for current_col, current_row in nodes_list:
#         point = [current_col, current_row]
#         for slope in node_slopes[f"{current_col}_{current_row}"]:
#             max_reach = get_furthest_reach(point, slope, size, size, edges)
#             if max_reach > 0:
#                 nodes_info[f"{current_col}_{current_row}"]["begin"].append(slope)
#                 for num in range(1, max_reach):
#                     new_col = current_col + num * slope[0]
#                     new_row = current_row + num * slope[1]
#                     try:
#                         node_slopes[f"{new_col}_{new_row}"].remove(slope)
#                     except ValueError: 
#                         pass
#                     nodes_info[f"{new_col}_{new_row}"]["middle"].append(slope)
#                 new_col = current_col + max_reach * slope[0]
#                 new_row = current_row + max_reach * slope[1]
#                 try:
#                     node_slopes[f"{new_col}_{new_row}"].remove(slope)
#                 except ValueError:
#                     pass
#                 nodes_info[f"{new_col}_{new_row}"]["end"].append(slope)
    
#     start = grid_info["start"]
#     target = grid_info["target"]
#     new_path = Path(__file__).parent/"Nodes_info"/f"Size{size}"/f"sample{index}.json"
#     if is_empty_dict(nodes_info[f"{start[0]}_{start[1]}"]) or is_empty_dict(nodes_info[f"{target[0]}_{target[1]}"]):
#         state = "invalid"
#     else: state = "valid"

#     info = {
#         "state": state,
#         "nodes_info": nodes_info,
#     }

#     with open(new_path, "w") as f:
#         json.dump(info, f, indent=1)

# Create Entirely_redundant_points_list and
# Active_nodes_info

def split_dict_key(key):
    """
    Convert dict key 'i_j' to list [i, j]
    """
    coords = key.split("_")
    return [int(coords[0]), int(coords[1])]

def refine_nodes_info_and_redundant_points_10_to_100():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            node_path = Path(__file__).parent/"Nodes_info"/f"Size{size}"/f"sample{index}.json"
            with open(node_path, "r") as f_in:
                nodes_info = json.load(f_in)["nodes_info"]

            active_nodes_dict = dict()
            entirely_redundant_points_list = []

            for key in nodes_info.keys():
                if is_empty_dict(nodes_info[key]):
                    entirely_redundant_points_list.append(split_dict_key(key))
                else:
                    active_nodes_dict[key] = nodes_info[key]

            active_nodes_path = Path(__file__).parent/"Active_nodes_info"/f"Size{size}"/f"sample{index}.json"
            entirely_redundant_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"

            redundant_dict = {
                "entirely_redundant_points_list": entirely_redundant_points_list
            }

            with open(active_nodes_path, "w") as f:
                json.dump(active_nodes_dict, f, indent=1)

            with open(entirely_redundant_path, "w") as f:
                json.dump(redundant_dict, f, indent=1)

# Create Adjacent_nodes and Reachable_nodes

# Adjacent_nodes
def generate_adjacent_nodes_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            adjacent_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Adjacent_nodes"/f"Size{size}"/f"sample{index}.json"
            active_nodes_path = Path(__file__).parent/"Active_nodes_info"/f"Size{size}"/f"sample{index}.json"
            entirely_redundant_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"

            adjacent_nodes_dict = dict()

            with open(active_nodes_path, "r") as f:
                active_nodes_info = json.load(f)

            with open(entirely_redundant_path, "r") as f:
                entirely_redundant_nodes = json.load(f)["entirely_redundant_points_list"]

            # Remove redundant nodes (nodes without adjacency)
            nodes_list = [[i, j] for j in range(1, size + 1) for i in range(1, size + 1)]
            for node in entirely_redundant_nodes:
                nodes_list.remove(node)

            # Update active_nodes_dict one by one through slope type
            for current_col, current_row in nodes_list:
                node_list = []
                slope_dict = active_nodes_info[f"{current_col}_{current_row}"]
                for slope in slope_dict["begin"]:
                    node_list.append([current_col + slope[0], current_row + slope[1]])
                for slope in slope_dict["middle"]:
                    node_list.append([current_col + slope[0], current_row + slope[1]])
                    node_list.append([current_col - slope[0], current_row - slope[1]])
                for slope in slope_dict["end"]:
                    node_list.append([current_col - slope[0], current_row - slope[1]])
                adjacent_nodes_dict[f"{current_col}_{current_row}"] = node_list

            with open(adjacent_nodes_path, "w") as f:
                json.dump(adjacent_nodes_dict, f, indent=1)

# Reachable nodes
def generate_reachable_nodes_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            reachable_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Reachable_nodes"/f"Size{size}"/f"sample{index}.json"
            active_nodes_path = Path(__file__).parent/"Active_nodes_info"/f"Size{size}"/f"sample{index}.json"
            entirely_redundant_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"
            edge_path = Path(__file__).parent/"Sorted_edge_list"/f"Size{size}"/f"sample{index}.json"
            
            with open(edge_path, "r") as f:
                edges = json.load(f)["edges"]

            with open(active_nodes_path, "r") as f:
                active_nodes_info = json.load(f)

            with open(entirely_redundant_path, "r") as f:
                entirely_redundant_nodes = json.load(f)["entirely_redundant_points_list"]

            # Remove redundant nodes (nodes without adjacency)
            nodes_list = [[i, j] for j in range(1, size + 1) for i in range(1, size + 1)]
            for node in entirely_redundant_nodes:
                nodes_list.remove(node)

            reachable_nodes_dict = {f"{current_col}_{current_row}": [] for current_col, current_row in nodes_list}

            # Update reachable_nodes_dict one by one through slope type
            for current_col, current_row in nodes_list:
                point = [current_col, current_row]
                begin_slopes = active_nodes_info[f"{current_col}_{current_row}"]["begin"]
                for slope in begin_slopes:
                    max_reach = get_furthest_reach(point, slope, size, size, edges)
                    furthest_point = [current_col + max_reach * slope[0], current_row + max_reach * slope[1]]
                    point_list = get_points_between(point, furthest_point)
                    for first_index in range(max_reach):
                        p1 = point_list[first_index]
                        for second_index in range(first_index + 1, max_reach + 1):
                            p2 = point_list[second_index]
                            reachable_nodes_dict[f"{p1[0]}_{p1[1]}"].append(p2)
                            reachable_nodes_dict[f"{p2[0]}_{p2[1]}"].append(p1)
                
            with open(reachable_nodes_path, "w") as f:
                json.dump(reachable_nodes_dict, f, indent=1)

# Inadjacent and unreachable nodes: Get the remainder
# Inadjacent nodes
def generate_inadjacent_nodes_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            inadjacent_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Inadjacent_nodes"/f"Size{size}"/f"sample{index}.json"
            entirely_redundant_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"
            adjacent_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Adjacent_nodes"/f"Size{size}"/f"sample{index}.json"

            with open(entirely_redundant_path, "r") as f:
                entirely_redundant_nodes = json.load(f)["entirely_redundant_points_list"]

            with open(adjacent_nodes_path, "r") as f:
                adjacent_nodes = json.load(f)
            
            # Remove redundant nodes (nodes without adjacency)
            nodes_list = [[i, j] for j in range(1, size + 1) for i in range(1, size + 1)]
            for node in entirely_redundant_nodes:
                nodes_list.remove(node)

            inadjacent_nodes_dict = dict()
            # Update inadjacent_dict by getting the remainder of nodes_list for each node
            for current_col, current_row in nodes_list:
                temp = nodes_list.copy()
                removed_nodes = adjacent_nodes[f"{current_col}_{current_row}"]
                for node in removed_nodes:
                    temp.remove(node)
                inadjacent_nodes_dict[f"{current_col}_{current_row}"] = temp

            with open(inadjacent_nodes_path, "w") as f:
                json.dump(inadjacent_nodes_dict, f, indent=1)

# Unreachable nodes
def generate_unreachable_nodes_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(4, 11):
            unreachable_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Unreachable_nodes"/f"Size{size}"/f"sample{index}.json"
            entirely_redundant_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"
            reachable_nodes_path = Path(__file__).parent/"Modeling_purpose"/"Reachable_nodes"/f"Size{size}"/f"sample{index}.json"

            with open(entirely_redundant_path, "r") as f:
                entirely_redundant_nodes = json.load(f)["entirely_redundant_points_list"]

            with open(reachable_nodes_path, "r") as f:
                reachable_nodes = json.load(f)
            
            # Remove redundant nodes (nodes without adjacency)
            nodes_list = [[i, j] for j in range(1, size + 1) for i in range(1, size + 1)]
            for node in entirely_redundant_nodes:
                nodes_list.remove(node)

            unreachable_nodes_dict = dict()
            # Update unreachable_dict by getting the remainder of nodes_list for each node
            for current_col, current_row in nodes_list:
                temp = nodes_list.copy()
                removed_nodes = reachable_nodes[f"{current_col}_{current_row}"]
                for node in removed_nodes:
                    temp.remove(node)
                unreachable_nodes_dict[f"{current_col}_{current_row}"] = temp

            with open(unreachable_nodes_path, "w") as f:
                json.dump(unreachable_nodes_dict, f, indent=1)

generate_unreachable_nodes_10_to_40()