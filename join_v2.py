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

    if source==target:
        #complete network things



    else:
        for i in range(len(joinBy)):
            if joinBy[i]['attr']=="":
                pairs = list(cur.execute(f'SELECT {source}, {target} from T'))
            else:
                pairs = list(cur.execute(f'SELECT {source}, {target} from T'))
            temp = nx.Graph()
            temp.add_edges_from(pairs)
            graphs.append(temp)

    return nx.compose_all(graphs)