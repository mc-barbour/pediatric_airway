import numpy as np
import vtk
import glob
from read_vtk import *
from natsort import natsorted
from surf_slice import slice_extract
import plotly.graph_objects as go



files = glob.glob('../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/*.vtk')
files=natsorted(files)

plane_center=(-2.251,-288.365,-165.872)
N=(.04,-0.8,0.5)

plane=vtkPlane()
plane.SetOrigin(plane_center)
plane.SetNormal(N[0],N[1],N[2])


#Load first file to access number of points
reader=vtkDataSetReader()
reader.SetFileName(files[0])
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

#Load the data
data = reader.GetOutput()

cutEdges = vtk.vtkCutter()
cutEdges.SetInputData(data)
cutEdges.SetCutFunction(plane)
cutEdges.GenerateCutScalarsOn()
cutEdges.GenerateTrianglesOn()
# cutEdges.SetValue(0, 0.5)
cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutEdges.GetOutputPort())
cutStrips.Update()
cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())


# Extract boundary from cutPoly
cutBoundary = vtk.vtkFeatureEdges()
cutBoundary.SetInputData(cutPoly)
cutBoundary.Update()

# 1. Triangulate the surface - vtktriangle

deluanay = vtkDelaunay2D()
deluanay.SetInputData(cutPoly)

massFilter=vtkMassProperties()
massFilter.SetInputConnection(deluanay.GetOutputPort())
massFilter.Update()
area=massFilter.GetSurfaceArea()
print(area)

# 2. Compute the area - vtkMassProperties

pts=cutPoly.GetPoints()
n=cutPoly.GetNumberOfPoints()

X = np.zeros((3,n))
for i in range(n):
	p=pts.GetPoint(i)
	X[0,i]=p[0]
	X[1,i]=p[1]
	X[2,i]=p[2]

# fig=go.Figure()
# fig.add_trace(go.Scatter3d(x=X[0,:],y=X[1,:],z=X[2,:],mode="markers"))
# fig.show()


plane_mapper=vtk.vtkPolyDataMapper()
plane_mapper.SetInputConnection(deluanay.GetOutputPort())

#create plane actor
planeActor=vtk.vtkActor()
planeActor.SetMapper(plane_mapper)
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(planeActor)
renderWindow.Render()
renderWindowInteractor.Start()

