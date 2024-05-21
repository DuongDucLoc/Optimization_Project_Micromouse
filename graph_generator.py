from pathlib import Path
import json
from functools import cmp_to_key
import math

class Constant:
    """
    Turning time: After normalizing grid size to 1 and velcity to 1.
    Additional assumption: Turning time for acute angles 
    is twice as long as that for obtuse angles.
    """

    # Based on information in the video "The Fastest Maze-Solving Competition On Earth"
    # of channel Veritasium, from 10:40 to 11:20.
    acute =  7.5
    right_or_obtuse =  3.75

def get_Cartesian_length(slope, round_digit=5):
    """
    return Cartesian length of slope
    """
    a, b = slope[0], slope[1]
    return round(math.sqrt(a*a + b*b), round_digit)

def get_angle_cost(slope1, slope2):
    """
    return the cost between the two slopes (in their positive direction)    
    """
    inner_product = slope1[0] * slope2[0] + slope1[1] * slope2[1]
    if inner_product > 0: return [Constant.acute, Constant.right_or_obtuse]
    elif inner_product == 0: return [Constant.right_or_obtuse, Constant.right_or_obtuse]
    else: return [Constant.right_or_obtuse, Constant.acute]

def compare(node1, node2):
    """
    Compare nodes of the following structure
    node = "{col}_{row}_{slope_col}_{slope_row}_direction"
    return -1 if node1 < node2
    """
    list1 = [int(char) for char in node1.split("_")]
    list2 = [int(char) for char in node2.split("_")]
    if list1 < list2: return -1
    elif list1 == list2: return 0
    else: return 1

def check_validity(size, index):
    """
    Check validity of sample (size, index)
    """
    path = Path(__file__).parent/"Validity"/f"Size{size}"/f"sample{index}.txt"
    with open(path, "r") as f:
        text = f.readline()
    if text == "Invalid": return False
    else: return True

def split_dict_key(key):
    """
    Convert dict key 'i_j' to list [i, j]
    """
    coords = key.split("_")
    return [int(coords[0]), int(coords[1])]

# Generate dictionary to convert between abstract nodes and numbers
def generate_nodes_dictionary_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            if check_validity(size, index):
                dictionary_path = Path(__file__).parent/"Graphing_purpose"/"Nodes_dictionary"/f"Size{size}"/f"sample{index}.json"
                active_nodes_path = Path(__file__).parent/"Active_nodes_info"/f"Size{size}"/f"sample{index}.json"
                node_list = []
                with open(active_nodes_path, "r") as f:
                    active_nodes = json.load(f)
                for key, slopes in active_nodes.items():
                    for slope in slopes["begin"]:
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_1")
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_-1")
                    for slope in slopes["middle"]:
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_1")
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_-1")
                    for slope in slopes["end"]:
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_1")
                        node_list.append(key + f"_{slope[0]}_{slope[1]}_-1")
                node_list = sorted(node_list, key=cmp_to_key(compare))
                node_to_num_dict = dict()
                num_to_node_dict = dict()
                for i in range(len(node_list)):
                    node_to_num_dict[node_list[i]] = i
                    num_to_node_dict[i] = node_list[i]
                node_dict = {
                    "node_to_num": node_to_num_dict,
                    "num_to_node": num_to_node_dict,
                }
                with open(dictionary_path, "w") as f:
                    json.dump(node_dict, f, indent=1)

# Generate edges in graph
# To be run
# size = 40
# for index in range(5, 6):
#     if check_validity(size, index):
#         save_path = Path(__file__).parent/"Graphing_purpose"/"Save_graphs"/f"Size{size}"/f"sample{index}.json"
#         dictionary_path = Path(__file__).parent/"Graphing_purpose"/"Nodes_dictionary"/f"Size{size}"/f"sample{index}.json"
#         active_nodes_path = Path(__file__).parent/"Active_nodes_info"/f"Size{size}"/f"sample{index}.json"
#         segments_path = Path(__file__).parent/"Graphing_purpose"/"Segments_and_slopes"/f"Size{size}"/f"sample{index}.json"
#         grid_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"

#         # Grid_info for start and target points
#         with open(grid_path, "r") as f:
#             grid_info = json.load(f)
#         # Dictionary of nodes
#         with open(dictionary_path, "r") as f:
#             nodes_dict = json.load(f)["node_to_num"]
#         # Dictionary of active nodes and prime slopes
#         with open(active_nodes_path, "r") as f:
#             active_nodes = json.load(f)
#         # List of segment-and-slope(s)
#         with open(segments_path, "r") as f:
#             segments_and_slopes = json.load(f)

#         # Get start and target
#         start = grid_info["start"]
#         target = grid_info["target"]
#         start_key = f"{start[0]}_{start[1]}"
#         target_key = f"{target[0]}_{target[1]}"
#         start_slopes = active_nodes.pop(start_key)
#         target_slopes = active_nodes.pop(target_key)
#         edge_dict = dict()

#         start_slope_list = start_slopes["begin"] + start_slopes["middle"] + start_slopes["end"]
#         target_slope_list = target_slopes["begin"] + target_slopes["middle"] + target_slopes["end"]

#         # Add start and target to edge_dict
#         first_start = start_slope_list.pop(0)
#         first_start_key = start_key + f"_{first_start[0]}_{first_start[1]}_"
#         first_start_pos_key = str(nodes_dict[first_start_key + "1"])
#         first_start_neg_key = str(nodes_dict[first_start_key + "-1"])
#         edge_dict["start"] = first_start_pos_key

#         first_target = target_slope_list.pop(0)
#         first_target_key = target_key + f"_{first_target[0]}_{first_target[1]}_"
#         first_target_pos_key = str(nodes_dict[first_target_key + "1"])
#         first_target_neg_key = str(nodes_dict[first_target_key + "-1"])
#         edge_dict["target"] = first_target_pos_key

#         edges = dict()

#         # Add edges between the same nodes with different angles
#         # start and target: all edges are 0
#         for second_start in start_slope_list:
#             second_start_key = start_key + f"_{second_start[0]}_{second_start[1]}_"
#             second_start_pos_key = str(nodes_dict[second_start_key + "1"])
#             second_start_neg_key = str(nodes_dict[second_start_key + "-1"])
#             # Add edges
#             edges[first_start_pos_key + "_" + second_start_neg_key] = 0
#             edges[second_start_neg_key + "_" + first_start_pos_key] = 0
#             edges[first_start_neg_key + "_" + second_start_pos_key] = 0
#             edges[second_start_pos_key + "_" + first_start_neg_key] = 0
#             edges[first_start_pos_key + "_" + second_start_pos_key] = 0
#             edges[second_start_pos_key + "_" + first_start_pos_key] = 0
#             edges[first_start_neg_key + "_" + second_start_neg_key] = 0
#             edges[second_start_neg_key + "_" + first_start_neg_key] = 0

#         for second_target in target_slope_list:
#             second_target_key = target_key + f"_{second_target[0]}_{second_target[1]}_"
#             second_target_pos_key = str(nodes_dict[second_target_key + "1"])
#             second_target_neg_key = str(nodes_dict[second_target_key + "-1"])
#             # Add edges
#             edges[first_target_pos_key + "_" + second_target_neg_key] = 0
#             edges[second_target_neg_key + "_" + first_target_pos_key] = 0
#             edges[first_target_neg_key + "_" + second_target_pos_key] = 0
#             edges[second_target_pos_key + "_" + first_target_neg_key] = 0
#             edges[first_target_pos_key + "_" + second_target_pos_key] = 0
#             edges[second_target_pos_key + "_" + first_target_pos_key] = 0
#             edges[first_target_neg_key + "_" + second_target_neg_key] = 0
#             edges[second_target_neg_key + "_" + first_target_neg_key] = 0

#         for key, slopes in active_nodes.items():
#             begin_slopes = slopes["begin"]
#             middle_slopes = slopes["middle"]
#             end_slopes = slopes["end"]
#             begin_slope_length = len(begin_slopes)
#             middle_slopes_length = len(middle_slopes)
#             end_slopes_length = len(end_slopes)

#             # First loop
#             for i in range(begin_slope_length - 1):
#                 first_slope = slopes["begin"][i]
#                 first_slope_key = key + f"_{first_slope[0]}_{first_slope[1]}_"
#                 first_node_pos_key = str(nodes_dict[first_slope_key + "1"])
#                 first_node_neg_key = str(nodes_dict[first_slope_key + "-1"])
#                 for j in range(i + 1, begin_slope_length):
#                     #Initiate materials
#                     second_slope = slopes["begin"][j]
#                     angle_cost = get_angle_cost(first_slope, second_slope)[0]
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])

#                     # Add edges
#                     edges[second_node_neg_key + "_" + first_node_pos_key] = angle_cost
#                     edges[first_node_neg_key + "_" + second_node_pos_key] = angle_cost

#                 for second_slope in middle_slopes:
#                     costs = get_angle_cost(first_slope, second_slope)
#                     angle_cost = costs[0]
#                     other_angle_cost = costs[1]
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])

#                     # Add edges
#                     edges[second_node_neg_key + "_" + first_node_pos_key] = angle_cost
#                     edges[first_node_neg_key + "_" + second_node_pos_key] = angle_cost

#                     edges[second_node_pos_key + "_" + first_node_pos_key] = other_angle_cost
#                     edges[first_node_neg_key + "_" + second_node_neg_key] = other_angle_cost

#                 for second_slope in end_slopes:
#                     other_angle_cost = get_angle_cost(first_slope, second_slope)[1]
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])

#                     # Add edges
#                     edges[second_node_pos_key + "_" + first_node_pos_key] = other_angle_cost
#                     edges[first_node_neg_key + "_" + second_node_neg_key] = other_angle_cost

#             # Second loop
#             for i in range(middle_slopes_length - 1):
#                 first_slope = slopes["middle"][i]
#                 first_slope_key = key + f"_{first_slope[0]}_{first_slope[1]}_"
#                 first_node_pos_key = str(nodes_dict[first_slope_key + "1"])
#                 first_node_neg_key = str(nodes_dict[first_slope_key + "-1"])
#                 for j in range(i + 1, middle_slopes_length):
#                     second_slope = slopes["middle"][j]
#                     costs = get_angle_cost(first_slope, second_slope)
#                     angle_cost = costs[0]
#                     other_angle_cost = costs[1]
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])

#                     # Add edges
#                     edges[first_node_pos_key + "_" + second_node_neg_key] = angle_cost
#                     edges[second_node_neg_key + "_" + first_node_pos_key] = angle_cost
#                     edges[first_node_neg_key + "_" + second_node_pos_key] = angle_cost
#                     edges[second_node_pos_key + "_" + first_node_neg_key] = angle_cost

#                     edges[first_node_pos_key + "_" + second_node_pos_key] = other_angle_cost
#                     edges[second_node_pos_key + "_" + first_node_pos_key] = other_angle_cost
#                     edges[first_node_neg_key + "_" + second_node_neg_key] = other_angle_cost
#                     edges[second_node_neg_key + "_" + first_node_neg_key] = other_angle_cost

#                 for second_slope in end_slopes:
#                     costs = get_angle_cost(first_slope, second_slope)
#                     angle_cost = costs[0]
#                     other_angle_cost = costs[1]            
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])

#                     # Add edges
#                     edges[first_node_pos_key + "_" + second_node_neg_key] = angle_cost
#                     edges[second_node_pos_key + "_" + first_node_neg_key] = angle_cost

#                     edges[first_node_neg_key + "_" + second_node_neg_key] = other_angle_cost
#                     edges[second_node_pos_key + "_" + first_node_pos_key] = other_angle_cost

#             # Third loop
#             for i in range(end_slopes_length - 1):
#                 first_slope = slopes["end"][i]
#                 first_slope_key = key + f"_{first_slope[0]}_{first_slope[1]}_"
#                 first_node_pos_key = str(nodes_dict[first_slope_key + "1"])
#                 first_node_neg_key = str(nodes_dict[first_slope_key + "-1"])
#                 for j in range(i + 1, end_slopes_length):
#                     second_slope = slopes["end"][j]
#                     angle_cost = get_angle_cost(first_slope, second_slope)[0]
#                     second_slope_key = key + f"_{second_slope[0]}_{second_slope[1]}_"
#                     second_node_pos_key = str(nodes_dict[second_slope_key + "1"])
#                     second_node_neg_key = str(nodes_dict[second_slope_key + "-1"])            

#                     # Add edges
#                     edges[first_node_pos_key + "_" + second_node_neg_key] = angle_cost
#                     edges[second_node_pos_key + "_" + first_node_neg_key] = angle_cost

#         # Add edges between adjacent nodes
#         for segment_and_slope in segments_and_slopes:
#             segment = segment_and_slope["segment"]
#             slope = segment_and_slope["slope"]
#             slope_key = f"_{slope[0]}_{slope[1]}_"
#             unit_length = get_Cartesian_length(slope)
#             num_of_points = len(segment)
#             for i in range(num_of_points - 1):
#                 first_node = segment[i]
#                 first_point_key = f"{first_node[0]}_{first_node[1]}" + slope_key
#                 first_node_pos_key = str(nodes_dict[first_point_key + "1"])
#                 first_node_neg_key = str(nodes_dict[first_point_key + "-1"])

#                 second_node = segment[i + 1]
#                 second_point_key = f"{second_node[0]}_{second_node[1]}" + slope_key
#                 second_node_pos_key = str(nodes_dict[second_point_key + "1"])
#                 second_node_neg_key = str(nodes_dict[second_point_key + "-1"])

#                 # Add edges
#                 edges[first_node_pos_key + "_" + second_node_pos_key] = unit_length
#                 edges[second_node_neg_key + "_" + first_node_neg_key] = unit_length

#         edge_dict["edges"] = edges

#         with open(save_path, "w") as f:
#             json.dump(edge_dict, f)

# Generate another kind of graph

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

def generate_graph_two_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            grid_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"
            save_path = Path(__file__).parent/"Graphing_purpose"/"Save_graphs2"/f"Size{size}"/f"sample{index}.json"
            segment_and_slope_path = Path(__file__).parent/"Graphing_purpose"/"Segments_and_slopes"/f"Size{size}"/f"sample{index}.json"
            with open(segment_and_slope_path, "r") as f:
                segments_and_slopes = json.load(f)

            with open(grid_path, "r") as f:
                grid_info = json.load(f)
            
            start = coords_to_num(*grid_info["start"], size)
            target = coords_to_num(*grid_info["target"], size)

            edge_dict = {
                "start": start,
                "target": target
            }
            edge_list = []

            for segment_and_slope in segments_and_slopes:
                segment = segment_and_slope["segment"]
                slope = segment_and_slope["slope"]
                a, b = slope[0], slope[1]
                unit_length = get_Cartesian_length(slope)
                length = len(segment)
                for i in range(length - 1):
                    first_point = segment[i]
                    first_key = coords_to_num(*first_point, size)
                    second_point = segment[i + 1]
                    second_key = coords_to_num(*second_point, size)
                    edge_list.append([first_key, second_key, (unit_length, [a, b])])
                    edge_list.append([second_key, first_key, (unit_length, [-a, -b])])

            edge_dict["edges"] = edge_list
            with open(save_path, "w") as f:
                json.dump(edge_dict, f)
