import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages")
from pathlib import Path
from dijkstar import Graph, find_path
import json
import time

def check_validity(size, index):
    """
    Check validity of sample (size, index)
    """
    path = Path(__file__).parent/"Validity"/f"Size{size}"/f"sample{index}.txt"
    with open(path, "r") as f:
        text = f.readline()
    if text == "Invalid": return False
    else: return True

# Model 1
# size = 40
# for index in range(4, 5):
#     if check_validity(size, index):
#         save_path = Path(__file__).parent/"Graphing_purpose"/"Proposed_solutions"/f"Size{size}"/f"sample{index}.json"
#         edge_path = Path(__file__).parent/"Graphing_purpose"/"Save_graphs"/f"Size{size}"/f"sample{index}.json"
#         with open(edge_path, "r") as f:
#             edge_dict = json.load(f)

#         edges = edge_dict["edges"]
#         start = int(edge_dict["start"])
#         target = int(edge_dict["target"])

#         graph = Graph()
#         for key, value in edges.items():
#             nodes = key.split("_")
#             node1, node2 = int(nodes[0]), int(nodes[1])
#             graph.add_edge(node1, node2, value)

#         start_time = time.time()
#         try:
#             with open(save_path, "w") as f:
#                 json.dump(find_path(graph, start, target), f, indent=1)
#         except:
#             with open(save_path, "w") as f:
#                 json.dump(["No path found"], f)
#         runtime = time.time() - start_time

#         runtime_path = Path(__file__).parent/"Runtime"/f"Size{size}"/"Runtime.txt"
#         with open(runtime_path, "a") as f:
#             f.write(f"Sample {index}'s runtime: {runtime} (s)\n")

# Model 2
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

def get_angle_cost(slope1, slope2):
    """
    return the cost between the two slopes (in their positive direction)    
    """
    if slope1[0] * slope2[1] - slope1[1] * slope2[0] == 0: return 0
    else:
        inner_product = slope1[0] * slope2[0] + slope1[1] * slope2[1]
        if inner_product < 0: return Constant.acute
        else: return Constant.right_or_obtuse

def cost_function(u, v, edge, prev_edge):
    current_length, current_slope = edge
    if prev_edge:
        prev_slope = prev_edge[1]
    else:
        return current_length
    return current_length + get_angle_cost(prev_slope, current_slope)

# size = 4
# for size in [10*i for i in range(1, 5)]:
#     for index in range(4, 11):
#         if check_validity(size, index):
#             save_path = Path(__file__).parent/"Graphing_purpose"/"Proposed_solutions2"/f"Size{size}"/f"sample{index}.json"
#             edge_path = Path(__file__).parent/"Graphing_purpose"/"Save_graphs2"/f"Size{size}"/f"sample{index}.json"
#             with open(edge_path, "r") as f:
#                 edge_dict = json.load(f)

#             edges = edge_dict["edges"]
#             start = edge_dict["start"]
#             target = edge_dict["target"]

#             graph = Graph()
#             for edge_info in edges:
#                 graph.add_edge(*edge_info)

#         try:
#             with open(save_path, "w") as f:
#                 json.dump(find_path(graph, start, target, cost_func=cost_function), f, indent=1)
#         except:
#             with open(save_path, "w") as f:
#                 json.dump(["No path found"], f)