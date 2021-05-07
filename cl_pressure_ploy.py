
import glob
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px




cl_df = pd.read_csv("../Patient_Data/Pt109/Segmentations/Processed/Pt109_centerline.dat", delimiter=" ")
pressure_files = glob.glob("../Patient_Data/Pt109/Simulation/pressure*")

print(pressure_files)

cl_df["X"] = cl_df["X"]*1e-3
cl_df["Y"] = cl_df["Y"]*1e-3
cl_df["Z"] = cl_df["Z"]*1e-3

delta = np.sqrt(np.diff(cl_df["X"].values)**2 + np.diff(cl_df["Y"].values)**2 + np.diff(cl_df["Z"].values)**2)
distance = np.append(0, np.cumsum(delta))

colors = px.colors.qualitative.T10
plt = go.Figure()

name = ["Steady", "Steady - 'Surgery' ", "Unsteady"]
pressure_drop = np.zeros(len(name))
for i in range(len(pressure_files)):

    pressure = np.genfromtxt(pressure_files[i])
    pressure_drop[i] = pressure[0]
    plt.add_trace(go.Scatter(x=distance, y=pressure, name=name[i], line_width=4, marker_color=colors[i*3]))

plt.update_layout(template='plotly_white', title="Centerline Pressure, Peak Exhlale", font=dict(family="serif", size=18), width=800, height=400, legend=dict(orientation='h', yanchor='top', xanchor='right', y=1, x=1))
plt.update_yaxes(title="Pressure (Pa)")
plt.update_xaxes(title="Distance (m)")
plt.write_image("centerlin_pressure.png",scale=3)
plt.show()

plt = go.Figure()
plt.add_trace(go.Scatter3d(x=cl_df["X"], y=cl_df["Y"], z=cl_df["Z"], mode='markers+lines'))
plt.show()

print(pressure_drop)
print((pressure_drop[1] - pressure_drop[0]) / pressure_drop[0])

