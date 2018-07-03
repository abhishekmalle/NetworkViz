import sqlite3
import pandas as pd
import networkx as nx

from join import join1,join2


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
        G = nx.compose(G,join2(orClause['source'],
                              orClause['target'],
                              orClause['joinBy']))

    return G
