import streamlit as st
import hiplot as hip
import pandas as pd
import networkx as nx
import folium
import time
import io
from pyvis.network import Network

# Load HiPlot chart - reload causes entire widget to flicker
h = hip.Experiment.from_csv("hiplot-selected-6968.csv")
st.html(h.to_html(), height=700) #  key="a")

# Load Folium map - reload causes entire widget to flicker
m = folium.Map(location=[45.5236, -122.6750])
st.html(m._repr_html_(), height=700) #, key="y")

# Load Pyvis network
got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
got_net.barnes_hut()
got_data = pd.read_csv("https://www.macalester.edu/~abeverid/data/stormofswords.csv")

sources = got_data['Source']
targets = got_data['Target']
weights = got_data['Weight']
edge_data = zip(sources, targets, weights)

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]
    got_net.add_node(src, src, title=src)
    got_net.add_node(dst, dst, title=dst)
    got_net.add_edge(src, dst, value=w)

neighbor_map = got_net.get_adj_list()
for node in got_net.nodes:
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])

got_net.write_html("gameofthrones.html")
st.html(got_net.html, height=700)
