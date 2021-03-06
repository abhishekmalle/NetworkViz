from flask import Flask, request, render_template
import json
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

from flask_cors import cross_origin

import mod

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
@cross_origin()
def func():
    if request.method=='GET':
        return render_template('indexVis.html')
    else:
        query = json.loads(request.data)
        G = mod.parse(query)

        newG = nx.convert_node_labels_to_integers(G,label_attribute='label')
        temp = nx.node_link_data(G)

        ans = {}
        ans['nodes'] = temp['nodes']
        ans['links'] = []

        for link in temp['links']:
            a = {'from':link['source'], 'to':link['target']}
            ans['links'].append(a)

        for i in range(len(ans['nodes'])):
            ans['nodes'][i]['label'] = ans['nodes'][i]['id']

        return json.dumps(ans)

if __name__ == "__main__":
    app.run(debug=True,threaded=True,port=5000)
