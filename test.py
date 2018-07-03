import json
import networkx as nx
import matplotlib.pyplot as plt

import mod


with open("query1.json") as f:
    query = json.load(f)
    G = mod.parse(query)
    nx.draw(G, with_labels=True)
    plt.show()
    print('done')
