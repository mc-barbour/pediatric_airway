import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from vtk import *

def extract_polydata_coords(polydata):
    """ Extract polydata coordinates

    Input: polydata
    Output: array containing coordinates
    """
    num_points = polydata.GetNumberOfPoints()
    points = polydata.GetPoints()

    X = np.zeros((3,num_points))

    for point in range(num_points):
        p = points.GetPoint(point)
        X[0,point] = p[0]
        X[1,point] = p[1]
        X[2,point] = p[2]

    return X

def slice_area(cut_poly):
    """
    Compute the area contained with a contour curve using deluanay triangulation

    Input: polydata of 2D contour/cutplane
    Output: area (Scalar)
    """

	# Triangulate the surface
    deluanay = vtkDelaunay2D()
    deluanay.SetInputData(cut_poly)

	# Compute the surface area of the plane
    massFilter = vtkMassProperties()
    massFilter.SetInputConnection(deluanay.GetOutputPort())
    massFilter.Update()

    return massFilter.GetSurfaceArea()


def slice_extract(polydata, X0, N):
    """
    Extract a 2D slice from a 3D polydata surface.

    Input: model surface, origin of cut-plane, normal of cut-plane
    Output: Polydata of 2D cutplane (contour)
    """

	# Define cut plane
    plane = vtkPlane()
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

def apply_surface_displacement(surface, displacement):
    """
    Apply surface motion to polydata surface.

    Input: polydata surface, displacement array
    Ouput: updated surface
    """

	# Get the number of points on the surface
    npoints = surface.GetNumberOfPoints()

    # Get the surface points
    points = vtkPoints()
    points.ShallowCopy(surface.GetPoints())

    for i in range(npoints):
		# Create empty tuple
        p_new = [0,0,0]

		# Extract individual point
        p = points.GetPoint(i)

		# Apply displacement to each point
        p_new[0] = p[0] + displacement[0,i]
        p_new[1] = p[1] + displacement[1,i]
        p_new[2] = p[2] + displacement[2,i]

		# Set new points and update the
        surface.GetPoints().SetPoint(i, p_new)
        surface.GetPoints().Modified()

    surface.Modified()

    return surface

def plot_contour(contours, fig, num_contours, slices):
    """
    Plot contour slices.

    Input: contour Polydata, figure instance
    """
    num_contours = len(contours)

    for i in slices:

        X = extract_polydata_coords(contours[i])

        fig.add_trace(go.Scatter3d(x=X[0,:], y=X[1,:], z=X[2,:],mode='markers'))




def polydata_mesh_plot(surface, fig, opacity=0.2, color='grey'):
    """
    plot surface mesh from polydata using plotly

    Input: surface polydata, figure instance

    """
    X = extract_polydata_coords(surface)

    num_polys = surface.GetNumberOfCells()
    I = np.zeros(num_polys)
    J = np.zeros(num_polys)
    K = np.zeros(num_polys)

    for i in range(num_polys):
        cell = surface.GetCell(i)
        I[i] = cell.GetPointId(0)
        J[i] = cell.GetPointId(1)
        K[i] = cell.GetPointId(2)

    fig.add_trace(go.Mesh3d(x=X[0,:], y=X[1,:], z=X[2,:], i=I, j=J, k=K, opacity=opacity, color=color))

    return















