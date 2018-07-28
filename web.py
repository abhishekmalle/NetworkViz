from flask import Flask, request, render_template
import json
import networkx as nx
import matplotlib.pyplot as plt

import mod

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    query = json.loads(request.form['query'])
    G = mod.parse(query)
    return json.dumps(nx.node_link_data(G))
