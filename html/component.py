import streamlit as st
import hiplot as hip
import pandas as pd
import networkx as nx
import folium
import time
import io
from pyvis.network import Network
import state
from streamlit.ScriptRunner import StopException, RerunException

session_state = state.get(count=0)

def hiplot(height):
    # Load HiPlot chart - reload causes entire widget to flicker
    h = hip.Experiment.from_csv("hiplot-selected-6968.csv")
    return h.to_html(), height, "HiPlot Chart"

def folium_(height):
    # Load Folium map - reload causes entire widget to flicker
    m = folium.Map(location=[45.5236, -122.6750])
    return m._repr_html_(), height, "Folium Map"

def pyvis(height):
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
    return got_net.html, height, "Pyvis Network"

def display(args, subtitle=""):
    st.title(args[2])
    st.write(subtitle)
    st.html(args[0], height=args[1])
    "---"
        
if st.button("Next"):
    session_state.count += 1

if session_state.count == 1:
    display(hiplot(750))
if session_state.count == 2:
    display(folium_(None), "Height not auto set, chart is cutoff")
if session_state.count == 3:
    display(folium_(600), "Height set too long, whitespace exists below chart")
if session_state.count == 4:
    display(pyvis(700))
