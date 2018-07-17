# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 07:02:41 2018

@author: Abhishek
"""

import networkx as nx
import sqlite3

def join(source, target, joinBy):
    '''
    returns a graph of a single 'or' condition
    which may contain inner 'and' conditions
    '''

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    graphs = []
    G = nx.Graph()

    for i in range(len(joinBy)):
        pairs = list(cur.execute(f'SELECT {source}, {target} from T'))
        temp = nx.Graph()
        temp.add_edges_from(pairs)
        graphs.append(temp)

        if i==0:
            G = nx.compose_all(graphs)
        else:
            temp = nx.compose_all(graphs)
            G.add_nodes_from(temp.nodes)
            temp.add_nodes_from(G.nodes)
            G = nx.intersection(G,temp)

    return graphs[0]