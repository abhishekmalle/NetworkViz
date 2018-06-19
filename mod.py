import sqlite3
import pandas as pd
import networkx as nx


def load(fileName='testFile.csv', dbName='data.db'):
    conn = sqlite3.connect(dbName)
    csvDF = pd.read_csv(fileName)

    conn.execute('DROP TABLE IF EXISTS T')
    conn.commit()

    csvDF.to_sql(name='T', con=conn)

    conn.close()
    print(f'File loaded into {dbName}')


def parse(query):
    G = nx.Graph()

    for orClause in query:
        G = nx.compose(G,join(orClause['source'],
                              orClause['target'],
                              orClause['joinBy']))

    return G


def join(source, target, joinBy):
    '''
    returns a graph of a single 'or' condition
    which may contain inner 'and' conditions
    '''
    conn = sqlite3.connect('samp.db')
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
            G = nx.intersection(G,nx.compose_all(graphs))

    return G


