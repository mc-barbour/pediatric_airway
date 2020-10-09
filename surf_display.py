import numpy as np
from vtk import *
from read_vtk import *
import glob
from natsort import natsorted
import matplotlib.pyplot as plt
"""
Created by Michael Barbour. 10/2020

Script to read in vtk polydata with displacement scalars and visualize displacment magnitude.
Also can visualize cloud of polydata points specified by the user
"""

# Class for VTK point cloud

class vtkPointCloud:
	def __init__(self):
		self.vtkPolyData=vtkPolyData()
		self.initPoints()
		mapper=vtkPolyDataMapper()
		mapper.SetInputData(self.vtkPolyData)
		self.vtkActor = vtk.vtkActor()
		self.vtkActor.SetMapper(mapper)
		self.vtkActor.GetProperty().SetPointSize(5)

	def add_points(self,point):
		id = self.vtkPoints.InsertNextPoint(point)
		self.vtkCells.InsertNextCell(1)
		self.vtkCells.InsertCellPoint(id)
		self.vtkCells.Modified()
		self.vtkPoints.Modified()

	def initPoints(self):
		self.vtkPoints = vtk.vtkPoints()
		self.vtkCells = vtk.vtkCellArray()
		self.vtkPolyData.SetPoints(self.vtkPoints)
		self.vtkPolyData.SetVerts(self.vtkCells)


files = glob.glob('../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/*.vtk')
files=natsorted(files)


#Load first file to access number of points
reader=vtkDataSetReader()
reader.SetFileName(files[4])
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

#Load the data
data = reader.GetOutput()

#Get the number of points
Npoints = data.GetNumberOfPoints()
Nfiles = len(files)

#Create empty arrays - space,points,time
disp=np.zeros((3,Npoints,Nfiles))
X=np.zeros((3,Npoints,Nfiles))

# Load displacement and x-coordinates of the first image into arrays
disp[:,:,0],X[:,:,0] = extract_surface_data(files[0])

# Add displacement magnitude to use on surface contour
disp_mag=vtk.vtkDoubleArray()
disp_mag.SetNumberOfValues(Npoints)
data.GetPointData().SetScalars(disp_mag)

for i in range(Npoints):
	disp_mag.SetValue(i,np.sqrt(disp[0,i,0]**2 + disp[1,i,0]**2 + disp[2,i,0]**2))

# Create point cloud to overlay on surface
pointID=np.linspace(0,Npoints-1,int((Npoints-1)/10))
pointCloud = vtkPointCloud()
for i in pointID:
	pointCloud.add_points(X[:,i,0])

# Visualize
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(data)
else:
    mapper.SetInputData(data)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(2)

lut = vtk.vtkLookupTable()
lut.SetTableRange(0, 1)
lut.SetHueRange(0, 1)
lut.SetSaturationRange(1, 1)
lut.SetValueRange(1, 1)
lut.Build()


scalarbar=vtkScalarBarActor()
scalarbar.SetTitle("Displacement")
scalarbar.SetLookupTable(lut)
mapper.SetLookupTable(lut)


renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.AddActor2D(scalarbar)
renderer.AddActor(pointCloud.vtkActor)

renderWindow.Render()
renderWindowInteractor.Start()