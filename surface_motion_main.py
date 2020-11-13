import numpy as np
from vtk import *
from read_vtk import *
from surf_motion_functions import *
import glob
from natsort import natsorted
import plotly.graph_objects as go
import plotly.express as px



def main():
    """
    Script to visualize surface motion based on a displacement field. Output includes plot of area as a function of time and a movie of mesh motion

    """

	# Script Inputs
    MAKE_MOVIE = False
    surface_directory = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Attempt3/displacement_surfaces/'
    cl_file = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Segmentations/Processed/Pt109_centerline.dat'
    movie_dir = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Movie/'
    fig_dit = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Figures/'

    n_planes = 20

	# Load surface files and centerline file
    files = glob.glob(surface_directory + '*.vtk')
    files = natsorted(files)
    n_files = len(files)
    print("Number of files (time_steps): ", n_files)

    # Inverting between RTS and LPS (switching signs of first two components)
    x_cl = -np.genfromtxt(cl_file, skip_header=1, usecols=0)
    y_cl = -np.genfromtxt(cl_file, skip_header=1, usecols=1)
    z_cl = np.genfromtxt(cl_file, skip_header=1, usecols=2)
    print("Number of centerline data points:", len(x_cl))

	# Define plane centroids and normal vectors
    plane_ints = np.linspace(0, len(x_cl)-2, n_planes, dtype=int)
    plane_centroids = np.array(([x_cl[plane_ints], y_cl[plane_ints], z_cl[plane_ints]]))
    plane_normal_vectors = np.array(([x_cl[plane_ints+1] - x_cl[plane_ints], y_cl[plane_ints+1] - y_cl[plane_ints], z_cl[plane_ints+1] - z_cl[plane_ints]]))



    plane_area = np.zeros((n_files, n_planes))
    contours = np.empty(n_planes,dtype=object)



	# Main Loop - loop over surfaces and compute the motion
    for i in range(len(files)):
    # for i in range(5):
		# Open surface and displacement fields
        surface, displacment, X = extract_surface_data(files[i])

		# Apply surface displacment
        apply_surface_displacement(surface, displacment)

        # Make movie
        if MAKE_MOVIE:
            #camera=dict(eye = dict(x=1.5, y=0.0, z=0.0))
            camera=dict(eye = dict(x=0, y=0.0, z=1.5))
            surf_fig = go.Figure()
            polydata_mesh_plot(surface, surf_fig,  0.25, 'blue')
            surf_fig.update_layout(template='plotly_white',
                                scene_camera=camera)
            surf_fig.write_image(movie_dir+'frame_xy_'+str(i)+'.png',scale=3)

		# Extract contours - plane extract and compute area
        for j in range(n_planes):
            contour_polydata = slice_extract(surface, plane_centroids[:,j], plane_normal_vectors[:,j])
            plane_area[i,j]=slice_area(contour_polydata)
            contours[j] = contour_polydata


    # ================================================================
    # Figure Generation
    # ================================================================

    slices=np.array([1,2,4,8,9,10,12,13,17])
    fig = go.Figure()
    plot_contour(contours, fig, n_planes, slices)
    polydata_mesh_plot(surface, fig, opacity=0.1)
    fig.update_layout(template='plotly_white', title='Slice Locations')

    fig.show()


	# Plot the average mesh area in time - normalized
    fig = go.Figure()
    for i in slices:
        fig.add_trace(go.Scatter(y=plane_area[:,i]/np.mean(plane_area[:,i])))
    fig.update_layout(template='plotly_white', title='Slice Expansion')
    fig.update_yaxes(title=r'$\text{Area/Time-averaged Area}, A(t)/\bar{A(t)}$')
    fig.update_xaxes(title=r"$\text{Time Steps} (\cdot)$")
    fig.show()



    # Plot centerline and show the location of the planes with normal vectors
    fig = go.Figure()
    skip = 10
    fig.add_trace(go.Scatter3d(x=x_cl[::skip], y=y_cl[::skip], z=z_cl[::skip],marker_color='grey'))
    fig.add_trace(go.Cone(x=plane_centroids[0,:], y=plane_centroids[1,:], z=plane_centroids[2,:],
        u=plane_normal_vectors[0,:], v=plane_normal_vectors[1,:], w=plane_normal_vectors[2,:],
        sizemode='absolute',sizeref=0.5))
    polydata_mesh_plot(surface, fig, opacity=0.1)
    fig.update_layout(scene=dict(aspectmode='data',aspectratio=dict(x=1, y=1, z=1)), template='plotly_white',
        title="Surface Centerlines")
    fig.show()



    # Plot peak motion for all slices at the same instant in time
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=plane_area[15,:]/np.mean(plane_area,axis=0),mode='markers+lines'))
    fig.add_shape(type='line', x0=0, y0=1, x1=len(plane_area[15,:]), y1=1,
        line=dict(
            color="grey",
            width=4,
            dash="dashdot"))
    fig.update_layout(template='plotly_white', title='Peak Motion')
    fig.update_yaxes(title=r'$\text{Area/Time-averaged Area}, A(t)/\bar{A(t)}$')
    fig.update_xaxes(title='Length of Domain')
    fig.show()


if __name__ == "__main__":
    main()
