import json
from pathlib import Path
import matplotlib.pyplot as plt
import os

# path = Path(__file__).parent/"Image"

# fig, ax = plt.subplots(1, 1)
# ax.plot([0, 0], [1, 1], marker="o")
# ax.axis("scaled")
# fig.savefig(path/f"foo.png", bbox_inches='tight')
# plt.show()
# plt.close(fig)

# def split_dict_key(key):
#     """
#     Convert dict key 'i_j' to list [i, j]
#     """
#     coords = key.split("_")
#     return [int(coords[0]), int(coords[1])]

# print(split_dict_key("1_2"))

# a = {"a": 1}
# # print(a.keys())
# for key in a.keys():
#     print(key)

# path1 = Path(__file__).parent/"Modeling_purpose"/"Adjacent_nodes"
# path2 = Path(__file__).parent/"Modeling_purpose"/"Reachable_nodes"
# path3 = Path(__file__).parent/"Modeling_purpose"/"Unreachable_nodes"
# path4 = Path(__file__).parent/"Modeling_purpose"/"Inadjacent_nodes"

# for path in [path3, path4]:
#     for size in [10*i for i in range(1, 11)]:
#         new_path = path/f"Size{size}"
#         os.mkdir(new_path)