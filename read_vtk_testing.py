import numpy as np
from vtk import *
from read_vtk import *
import glob
from natsort import natsorted
import matplotlib.pyplot as plt

files = glob.glob('../Patient_Data/4DCT_109/Attempt3/displacement_surfaces/*.vtk')
files=natsorted(files)
print(files)


#Load first file to access number of points
reader=vtkDataSetReader()
reader.SetFileName(files[0])
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

# Load displacement and x-coordinates into arrays
for i in range(Nfiles):
	disp[:,:,i],X[:,:,i] = extract_surface_data(files[i])


pointID=50000


plt.figure()
plt.plot(np.sqrt(disp[0,pointID,:]**2+disp[1,pointID,:]**2+disp[2,pointID,:]**2))
plt.title("Displacement Magnitude of point "+str(pointID))
plt.show()