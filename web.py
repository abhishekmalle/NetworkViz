from flask import Flask, request, render_template
import json
import networkx as nx
import matplotlib.pyplot as plt

import mod

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('website.html')

@app.route('/', methods=['POST'])
def my_form_post():
    query = json.loads(request.form['text'])
    G = mod.parse(query)
    print(nx.node_link_data(G))
    return json.dumps(nx.node_link_data(G))
