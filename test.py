import json
from pathlib import Path
import matplotlib.pyplot as plt
import os

path = Path(__file__).parent/"Image"

fig, ax = plt.subplots(1, 1)
ax.plot([0, 0], [1, 1], marker="o")
ax.axis("scaled")
fig.savefig(path/f"foo.png", bbox_inches='tight')
plt.show()
plt.close(fig)