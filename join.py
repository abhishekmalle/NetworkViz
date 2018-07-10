 # -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 23:07:05 2018

@author: Abhishek
"""

import sqlite3
import networkx as nx

def join1(source, target, joinBy):
    '''
    returns a graph of a single 'or' condition
    which may contain inner 'and' conditions
    '''
    conn = sqlite3.connect('data.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    G = nx.Graph()

    for i in range(len(joinBy)):
        graphs = []

        if joinBy[i]['conditionType'] == 'categorical':
            if joinBy[i]['value'] == []:
                li = list(cur.execute(f'''
                                      SELECT DISTINCT {joinBy[i]["attr"]}
                                      FROM T
                                      '''))
            else:
                li = joinBy[i]['value']
            for val in li:
                graphs.append(nx.complete_graph(list(
                        cur.execute(f'''
                                    SELECT {source}
                                    FROM T
                                    WHERE {joinBy[i]["attr"]} = ?
                                    ''', [val]).fetchall())))
                print(f'{val} is complete-networked')

        if i==0:
            G = nx.compose_all(graphs)
        else:
            temp = nx.compose_all(graphs)
            G.add_nodes_from(temp.nodes)
            temp.add_nodes_from(G.nodes)
            G = nx.intersection(G,temp)

    return G

def join2(source, target, joinBy):
    '''
    returns a graph of a single 'or' condition
    which may contain inner 'and' conditions
    '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    G = nx.Graph()

    for i in range(len(joinBy)):
        graphs = []

        if source == target:
            return join1(source, target, joinBy)

        if joinBy[i]['value'] == []:
            conn.row_factory = lambda cursor, row: row[0]
            cur = conn.cursor()
            li = list(cur.execute(f'''
                                  SELECT DISTINCT {joinBy[i]["attr"]}
                                  FROM T
                                  '''))
            conn.row_factory = lambda cursor, row: row
            cur = conn.cursor()
        else:
            li = joinBy[i]['value']

        for val in li:
            x = nx.Graph()
            query = f'''SELECT {source}, {target}
                        FROM T
                        WHERE {joinBy[i]["attr"]} = ?
                        '''
            print(val)
            s = cur.execute(query, [val]).fetchall()
            print(s)
            x.add_edges_from(s)

            graphs.append(x)

        if i==0:
            G = nx.compose_all(graphs)
        else:
            G = nx.intersection(G,nx.compose_all(graphs))

    return G
