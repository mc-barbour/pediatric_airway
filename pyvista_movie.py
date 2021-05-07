import pyvista as pv
import glob


files = glob.glob('/Users/mbarbour/Dropbox/Respiratory/image_data/Pt_106/DisplacementSurfaces/*')


surface = pv.read(files[0])


# Create a plotter object and set the scalars to the Z height
plotter = pv.Plotter()
actor = plotter.add_mesh(surface, color='blue', smooth_shading=True)

print('Orient the view, then press "q" to close window and produce movie')

# setup camera and close
plotter.show(auto_close=False)

# Open a gif
plotter.open_gif("test.gif")

plotter.remove_actor(actor)
# Update Z and write a frame for each updated position
nframe = len(files)
for i in range(nframe):
    surface = pv.read(files[i])
    plotter.add_mesh(surface)

    # must update normals when smooth shading is enabled
    #plot``1`ter.mesh.compute_normals(cell_normals=False, inplace=True)
    plotter.write_frame()  # this will trigger the render

    # otherwise, when not writing frames, render with:
    # plotter.render()

# Close movie and delete object
plotter.close()

