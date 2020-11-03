import numpy as np
from vtk import *
from read_vtk import *
import glob
from natsort import natsorted
import plotly.graph_objects as go
import plotly.express as px

def slice_extract(polydata,X0,N):
	plane=vtkPlane()
	plane.SetOrigin(X0)
	plane.SetNormal(N[0],N[1],N[2])

	# Create a cutter
	cutter=vtkCutter()
	cutter.SetCutFunction(plane)
	cutter.SetInputData(polydata)
	cutter.Update()

	# Convert to PolyData
	stripper=vtkStripper()
	stripper.SetInputConnection(cutter.GetOutputPort())
	stripper.Update()

	# Extract points
	contour=vtkPolyData()
	contour=stripper.GetOutput()

	disp = contour.GetPointData().GetArray('NRRDImage')	
	contour_points = contour.GetPoints()
	
	return disp, contour_points, cutter


files = glob.glob('../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/*.vtk')
files=natsorted(files)
print(files)

Nfiles = len(files)

colors=px.colors.cyclical.IceFire
# colors=np.append(colors,colors)
print(len(colors))

# Extract slice from every time step
fig=go.Figure()
for i in range(8):
	reader=vtkDataSetReader()
	reader.SetFileName(files[i])
	reader.ReadAllVectorsOn()
	reader.ReadAllScalarsOn()
	reader.Update()

	# Load the data
	data = reader.GetOutput()

	# Get the number of points
	plane_center=(-2.251,-288.365,-165.872)
	plane_normal=(.04,-0.8,0.5)

	contour_disp,contour_points,cutter = slice_extract(data,plane_center,plane_normal)
	Npoints = contour_points.GetNumberOfPoints()
	
	X=np.zeros((3,Npoints))
	for j in range(Npoints):
		p=contour_points.GetPoint(j)
		X[0,j] = p[0]+contour_disp.GetComponent(j,0)
		X[1,j] = p[1]+contour_disp.GetComponent(j,1)
		X[2,j] = p[2]+contour_disp.GetComponent(j,2)


	fig.add_trace(go.Scatter3d(x=X[0,:],y=X[1,:],z=X[2,:],mode="markers",marker_color=colors[i]))

fig.update_layout(scene=dict(aspectmode='data',aspectratio=dict(x=1,y=1,z=1)))
fig.show()



# Visualize Slice

cutterMapper=vtk.vtkPolyDataMapper()
cutterMapper.SetInputConnection(cutter.GetOutputPort())

#create plane actor
planeActor=vtk.vtkActor()
planeActor.GetProperty().SetColor(255,255,255)
planeActor.GetProperty().SetLineWidth(20)
planeActor.SetMapper(cutterMapper)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(data)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(2)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.AddActor(planeActor)

renderWindow.Render()
renderWindowInteractor.Start()

