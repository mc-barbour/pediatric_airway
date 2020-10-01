import numpy as np
from vtk import *
"""
Function to read vtk surface file and extract the coordinates and displacement values
"""

def extract_surface_data(filename):
	#Set details for the loader
	reader=vtkDataSetReader()
	reader.SetFileName(filename)
	reader.ReadAllVectorsOn()
	reader.ReadAllScalarsOn()
	reader.Update()

	#Load the data
	data = reader.GetOutput()

	#Get the number of points
	Npoints = data.GetNumberOfPoints()

	#Get the data arrays (NRRDImage is the tuple array)
	NRRDImage = data.GetPointData().GetArray('NRRDImage')
	vtkValidPointMask = data.GetPointData().GetArray('vtkValidPointMask')

	#Get the points - to extract the coordinates
	points=data.GetPoints()

	#Copy the stored data into numpy arrays
	X = np.zeros((3,Npoints))
	disp = np.zeros((3,Npoints))
	for i in range(Npoints):
	    disp[0,i] = NRRDImage.GetComponent(i,0)
	    disp[1,i] = NRRDImage.GetComponent(i,1)
	    disp[2,i] = NRRDImage.GetComponent(i,2)
	    p=points.GetPoint(i)
	    X[0,i] = p[0]
	    X[1,i] = p[1]
	    X[2,i] = p[2]

	return(disp,X)

