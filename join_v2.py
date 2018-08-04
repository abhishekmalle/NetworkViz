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
    intersectGraphs = []

    if source==target:
        for i in range(len(joinBy)): # "and" conditions (intersections)
            # assumes that there has to be an "attr"
            composeGraphs = []
            if joinBy[i]['value']==[]:
                a = list(cur.execute(f'''
                             SELECT GROUP_CONCAT({source}), {joinBy[i]["attr"]}
                             FROM T
                             GROUP BY {joinBy[i]["attr"]}
                             '''))
                for tup in a:
                    nodes = [x.strip() for x in tup[0].split(',')]
                    composeGraphs.append(nx.complete_graph(nodes))

            else:
                li = joinBy[i]['value']
                for val in li:
                    a = list(cur.execute(f'''
                                     SELECT GROUP_CONCAT({source}), {joinBy[i]["attr"]}
                                     FROM T
                                     WHERE {joinBy[i]["attr"]}=?
                                     GROUP BY {joinBy[i]["attr"]}
                                     ''', [val]))

                    nodes = [x.strip() for x in a[0][0].split(',')]
                    composeGraphs.append(nx.complete_graph(nodes))

            # adding a graph from a single joinBy condition
            intersectGraphs.append(nx.compose_all(composeGraphs))

    else:
        for i in range(len(joinBy)):
            if joinBy[i]['attr']=='':
                pairs = list(cur.execute(f'SELECT {source}, {target} from T'))
            else:
                if joinBy[i]['value']==[]:
                    li = list(cur.execute(f'''
                                      SELECT DISTINCT {joinBy[i]["attr"]}
                                      FROM T
                                      '''))
                else:
                    li = joinBy[i]['value']

                for val in li:
                    pairs = list(cur.execute(f'''
                                             SELECT {source}, {target}
                                             FROM T
                                             WHERE {joinBy[i]["attr"]}=?
                                             ''', [val]))
            temp = nx.Graph()
            for p in pairs:
                temp.add_node(p[0], type=source, color="blue")
                temp.add_node(p[1], type=target, color="red")
            temp.add_edges_from(pairs)
            intersectGraphs.append(temp)

    for i in range(len(intersectGraphs)):
        if i>0:
            intersectGraphs[i].add_nodes_from(intersectGraphs[i-1])
    G = nx.intersection_all(intersectGraphs)
    G.remove_nodes_from(list(nx.isolates(G)))
    return G
