import numpy as np
from vtk import *
from read_vtk import *
from surf_motion_functions import *
import glob
from natsort import natsorted
import plotly.graph_objects as go
import plotly.express as px

def plot_contour(contours,fig):
	points = contours.GetPoints()
	npoints=contours.GetNumberOfPoints()
	X=np.zeros((3,npoints))
	for i in range(npoints):
		p=points.GetPoint(i)
		X[0,i] = p[0]
		X[1,i] = p[1]
		X[2,i] = p[2]
	fig.add_trace(go.Scatter3d(x=X[0,:],y=X[1,:],z=X[2,:]))


# Scrtipt inputs
surface_directory = '../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/'
cl_file='/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Segmentations/Processed/Pt109_centerline.dat'
n_planes = 20


# Load surface files and centerline file
files = glob.glob(surface_directory + '*.vtk')
files=natsorted(files)
n_files=len(files)
print("Number of files (time_steps): ",n_files)

x_cl = -np.genfromtxt(cl_file,skip_header=1,usecols=0) # Inverting between RTS and LPS (switching signs of first two components)
y_cl = -np.genfromtxt(cl_file,skip_header=1,usecols=1) 
z_cl = np.genfromtxt(cl_file,skip_header=1,usecols=2)
print("Number of centerline data points:",len(x_cl))

# Define plane centroids and normal vectors
plane_ints = np.linspace(0,len(x_cl)-2,n_planes,dtype=int)
plane_centroids = np.array(([x_cl[plane_ints],y_cl[plane_ints],z_cl[plane_ints]]))
plane_normal_vectors=np.array(([x_cl[plane_ints+1] - x_cl[plane_ints],y_cl[plane_ints+1] - y_cl[plane_ints],z_cl[plane_ints+1] - z_cl[plane_ints]]))

# Plot Centerline and show the location of the planes with normal vectors
fig=go.Figure()
skip=10
fig.add_trace(go.Scatter3d(x=x_cl[::skip],y=y_cl[::skip],z=z_cl[::skip],marker_color='grey'))
fig.add_trace(go.Cone(x=plane_centroids[0,:],y=plane_centroids[1,:],z=plane_centroids[2,:],
	u=plane_normal_vectors[0,:],v=plane_normal_vectors[1,:],w=plane_normal_vectors[2,:],
	sizemode='absolute',sizeref=0.5))
fig.update_layout(scene=dict(aspectmode='data',aspectratio=dict(x=1,y=1,z=1)),template='plotly_white',
	title="Surface Centerlines and Slice Locations")
fig.show()

plane_area = np.zeros((n_files,n_planes))
fig=go.Figure()
# Main Loop - loop over surfaces and compute the motion
for i in range(len(files)):
	# Open surface and displacement fields
	surface,displacment,X = extract_surface_data(files[i])

	# Apply surface displacment
	apply_surface_displacement(surface,displacment)

	# Extract contours - plane extract and compute area
	for j in range(n_planes):
		contour_polydata = slice_extract(surface,plane_centroids[:,j],plane_normal_vectors[:,j])
		plane_area[i,j]=slice_area(contour_polydata)
		if i==0:
		 	plot_contour(contour_polydata,fig)
fig.show()


fig=go.Figure()
for i in range(8,13):
	fig.add_trace(go.Scatter(y=plane_area[:,i]/np.mean(plane_area[:,i])))
fig.update_layout(template='plotly_white')
fig.update_yaxes(title=r'$\text{Area/Time-averaged Area}, A(t)/\bar{A(t)}$')
fig.update_xaxes(title=r"$\text{Time Steps} (\cdot)$")
fig.show()