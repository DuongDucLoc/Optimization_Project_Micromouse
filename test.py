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

point1, point2 = [4, 1], [4, 2]
edge = [[4, 3], [4, 4]]
print(check_intersection(point1, point2, edge))