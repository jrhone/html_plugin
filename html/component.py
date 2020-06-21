import streamlit as st
import hiplot as hip
import folium
import nglview
import time
import io

# Need full screen support on html
# Need refresh without reloading components

# Load HiPlot chart - reload causes entire widget to flicker
h = hip.Experiment.from_csv("hiplot-selected-6968.csv")
st.html(h.to_html(), height=700) #  key="a")

# Load Folium map - reload causes entire widget to flicker
m = folium.Map(location=[45.5236, -122.6750])
st.html(m._repr_html_(), height=700) #, key="y")

# Load NGLView - jupyter notebook widget, some script loading issue
output = io.StringIO()
view = nglview.show_pdbid('1tsu')
nglview.write_html(output, [view])
st.html(output.getvalue())
