import json
from pathlib import Path
import matplotlib.pyplot as plt
import os
from functools import cmp_to_key

# Check validity of samples
def generate_validity_10_to_40():
    for size in [10*i for i in range(1, 5)]:
        for index in range(1, 11):
            grid_path = Path(__file__).parent/"Samples"/f"Size{size}"/f"sample{index}.json"
            redundant_points_path = Path(__file__).parent/"Entirely_redundant_points_list"/f"Size{size}"/f"sample{index}.json"

            with open(grid_path, "r") as f:
                grid_info = json.load(f)

            with open(redundant_points_path, "r") as f:
                redundant_points_list = json.load(f)["entirely_redundant_points_list"]

            start = grid_info["start"]
            target = grid_info["target"]
            text_path = Path(__file__).parent/"Validity"/f"Size{size}"/f"sample{index}.txt"

            if (start in redundant_points_list) or (target in redundant_points_list):
                with open(text_path, "w") as f:
                    f.write("Invalid")
            else:
                with open(text_path, "w") as f:
                    f.write("Valid")

# size, index = 30, 1
# node_dict_path = Path(__file__).parent/"Graphing_purpose"/"Nodes_dictionary"/f"Size{size}"/f"sample{index}.json"
# with open(node_dict_path, "r") as f:
#     print(len(json.load(f)["node_to_num"].keys()))

# for size in [4] + [10*i for i in range(1, 5)]:
#     save_path = Path(__file__).parent/"Graphing_purpose"/"Proposed_solutions2"/f"Size{size}"
#     os.mkdir(save_path)