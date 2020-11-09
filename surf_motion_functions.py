import numpy as np
from vtk import *


def slice_area(cut_poly):

	# Triangulate the surface
	deluanay = vtkDelaunay2D()	
	deluanay.SetInputData(cut_poly)

	# Compute the surface area of the plane
	massFilter=vtkMassProperties()
	massFilter.SetInputConnection(deluanay.GetOutputPort())
	massFilter.Update()

	return massFilter.GetSurfaceArea()


def slice_extract(polydata,X0,N):

	# Define cut plane
	plane=vtkPlane()
	plane.SetOrigin(X0)
	plane.SetNormal(N[0],N[1],N[2])

	# Define cutter
	cutEdges = vtk.vtkCutter()
	cutEdges.SetInputData(polydata)
	cutEdges.SetCutFunction(plane)
	cutEdges.GenerateCutScalarsOn()
	cutEdges.GenerateTrianglesOn()

	# Define Stripper
	cutStrips = vtk.vtkStripper()
	cutStrips.SetInputConnection(cutEdges.GetOutputPort())
	cutStrips.Update()

	# Create Polydata
	cutPoly = vtk.vtkPolyData()
	cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
	cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

	return cutPoly

def apply_surface_displacement(surface,displacement):

	# Get the number of points on the surface
	npoints = surface.GetNumberOfPoints()

	# Get the surface points
	points=vtkPoints()
	points.ShallowCopy(surface.GetPoints())

	for i in range(npoints):
		# Create empty tuple
		p_new = [0,0,0]

		# Extract individual point
		p = points.GetPoint(i)

		# Apply displacement to each point
		p_new[0] = p[0]+displacement[0,i]
		p_new[1] = p[1]+displacement[1,i]
		p_new[2] = p[2]+displacement[2,i]

		# Set new points and update the 
		surface.GetPoints().SetPoint(i,p_new)
		surface.GetPoints().Modified()

	surface.Modified()

	return surface



















