import numpy as np
from vtk import *
from read_vtk import *
import glob

files = glob.glob('../Patient_Data/4DCT_109/Attempt3/*.vtk')
print(files)


disp0, X0 = extract_surface_data(files[0])
disp1, X1 = extract_surface_data(files[1])
disp2, X2 = extract_surface_data(files[2])

print(disp0[:,4000],disp1[:,4000],disp2[:,4000])
print(X1[:,4000],X2[:,4000])
