import pyvista as pv
from pathlib import Path
import glob

patients = [106, 109, 110]

data_dir = "/Users/mbarbour/Dropbox/Respiratory/image_data/"

p = pv.Plotter(shape=(1,3))

count = 0
for patient in patients:
    patient_str = "Pt_" + str(patient)
    surface_file = glob.glob(data_dir + patient_str + "/*.stl")

    surface = pv.read(surface_file)

    p.subplot(0, count)
    p.add_mesh(surface)
    p.add_text(str(patient))

    count=count+1

p.show()
