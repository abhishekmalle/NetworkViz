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
    # query = json.loads(request.form['query'])
    # G = mod.parse(query)
    # return json.dumps(nx.node_link_data(G))
    pprint(request.data)
    return '{"ADSF":"FDS"}'
