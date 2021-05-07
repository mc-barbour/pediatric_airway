# -*- coding: utf-8 -*-
"""
tecplot - probe volume along points

written: Michael Barbour

"""
import pandas as pd
import numpy as np
import tecplot as tp


import plotly.graph_objects as go

tp.session.connect()
tp.session.suspend()


# filename = '../Patient_Data/Pt109/Simulation/Pt109_730kelements_low-y+_unsteady@4.00001e+00.plt'


# dataset = tp.data.load_tecplot(filename)

frame = tp.active_frame()
# Load the centerline data - extraction points

cl_df = pd.read_csv("../Patient_Data/Pt109/Segmentations/Processed/Pt109_centerline.dat", delimiter=" ")

cl_df["X"] = cl_df["X"]*1e-3
cl_df["Y"] = cl_df["Y"]*1e-3
cl_df["Z"] = cl_df["Z"]*1e-3


pressure = np.zeros(len(cl_df))

for i in range(len(cl_df)):

    x = cl_df["X"][i]
    y = cl_df["Y"][i]
    z = cl_df["Z"][i]

    result = tp.data.query.probe_at_position(x, y, z)
    print(result)
    data, zone, frame = result

    pressure[i] = data[21]

np.savetxt("pressure_cl_steady_peak_exhale_surg1.txt", pressure)

fig = go.Figure()
fig.add_trace(go.Scatter(y=pressure))

fig.show()
