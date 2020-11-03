import numpy as np
import vtk
import glob
from read_vtk import *
from natsort import natsorted
from surf_slice import slice_extract
import plotly.graph_objects as go



files = glob.glob('../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/*.vtk')
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
disp,X_coord = extract_surface_data(files[0])


# # Deifne Plane
plane_center=(-2.251,-270.365,-170.872)
plane_normal=(.04,-0.8,0.5)
# plane_center=(-2.251,-288.365,-165.872)

# Extract plane
contour_disp,contour_points,cutter = slice_extract(data,plane_center,plane_normal)
print(contour_points.GetPoint(4))
n_contour_points = contour_points.GetNumberOfPoints()

fig=go.Figure()
X=np.zeros((3,n_contour_points))
for j in range(n_contour_points):
	c=contour_points.GetPoint(j)
	X[0,j] = c[0]+contour_disp.GetComponent(j,0)
	X[1,j] = c[1]+contour_disp.GetComponent(j,1)
	X[2,j] = c[2]+contour_disp.GetComponent(j,2)
fig.add_trace(go.Scatter3d(x=X[0,:],y=X[1,:],z=X[2,:],mode="markers"))

print(data.GetPoints().GetPoint(500))

#Get the number of points
Npoints = data.GetNumberOfPoints()

# #Get the points - to extract the coordinates
points= vtkPoints()
points.ShallowCopy(data.GetPoints())

for i in range(Npoints):
	p_new = [0,0,0]
	p = points.GetPoint(i)
	p_new[0] = p[0]+disp[0,i]
	p_new[1] = p[1]+disp[1,i]
	p_new[2] = p[2]+disp[2,i]
	data.GetPoints().SetPoint(i,p_new)
	data.GetPoints().Modified()

data.Modified()
print(data.GetPoints().GetPoint(500))

contour_disp,contour_points,cutter = slice_extract(data,plane_center,plane_normal)
print(contour_points.GetPoint(4))

n_contour_points = contour_points.GetNumberOfPoints()
X=np.zeros((3,n_contour_points))
for j in range(n_contour_points):
	c=contour_points.GetPoint(j)
	X[0,j] = c[0]+contour_disp.GetComponent(j,0)
	X[1,j] = c[1]+contour_disp.GetComponent(j,1)
	X[2,j] = c[2]+contour_disp.GetComponent(j,2)


fig.add_trace(go.Scatter3d(x=X[0,:],y=X[1,:],z=X[2,:],mode="markers"))
fig.update_layout(scene=dict(aspectmode='data',aspectratio=dict(x=1,y=1,z=1)))
fig.show()

#Display

# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputData(data)

# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# # actor.GetProperty().SetPointSize(2)

# renderer = vtk.vtkRenderer()
# renderWindow = vtk.vtkRenderWindow()
# renderWindow.AddRenderer(renderer)
# renderWindowInteractor = vtk.vtkRenderWindowInteractor()
# renderWindowInteractor.SetRenderWindow(renderWindow)

# renderer.AddActor(actor)

# renderWindow.Render()
# renderWindowInteractor.Start()







