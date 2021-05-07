import numpy as np
from vtk import *
from read_vtk import *
import glob
from natsort import natsorted
import matplotlib.pyplot as plt
import plotly.graph_objects as go

files = glob.glob('../Patient_Data/Pt109/Attempt3/displacement_surfaces/*.vtk')
#files = glob.glob('/Users/mbarbour/Dropbox/Respiratory/image_data/Pt_106/DisplacementSurfaces/*')
files=natsorted(files)
print(files)


#Load first file to access number of points
reader=vtkDataSetReader()
reader.SetFileName(files[0])
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

#Load the data
data = reader.GetOutput()

#print(data)

#Get the number of points
Npoints = data.GetNumberOfPoints()
Nfiles = len(files)

#Create empty arrays - space,points,time
disp=np.zeros((3,Npoints,Nfiles))
X=np.zeros((3,Npoints,Nfiles))

# Load displacement and x-coordinates into arrays
for i in range(Nfiles):
	surface,disp[:,:,i],X[:,:,i] = extract_surface_data(files[i])


pointID=50000



num_polys=surface.GetNumberOfCells()
I=np.zeros(num_polys)
J=np.zeros(num_polys)
K=np.zeros(num_polys)

for i in range(num_polys):
	cell = surface.GetCell(i)
	I[i]=cell.GetPointId(0)
	J[i]=cell.GetPointId(1)
	K[i]=cell.GetPointId(2)

fig=go.Figure()
fig.add_trace(go.Mesh3d(x=X[0,:,0],y=X[1,:,0],z=X[2,:,0],i=I,j=J,k=K,opacity=0.8))

camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=-1.35, y=1.25, z=1.25)
)
fig.update_layout(scene_camera=camera)

fig.show()



# celldata = surface.GetPolys()
# polys=celldata.GetData()
# print(polys.GetValue(0))
# plt.figure()
# plt.plot(np.sqrt(disp[0,pointID,:]**2+disp[1,pointID,:]**2+disp[2,pointID,:]**2))
# plt.title("Displacement Magnitude of point"+str(pointID))
# plt.ylabel("Displacement (mm)")
# plt.xlabel("Image")


# fig=go.Figure()
# fig.add_trace(go.Cone(x=X[0,:,0],y=X[1,:,0],z=X[2,:,0],u=disp[0,:,2],v=disp[1,:,2],w=disp[2,:,2],sizemode='absolute',sizeref=10))
# fig.show()

