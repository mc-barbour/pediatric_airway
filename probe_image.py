import numpy as np
from vtk import *
import nrrd

#Read raw image data
filename='../4DCT_109/3DImages/Attempt2/DisplacementField.nrrd'
data,header = nrrd.read(filename)

print(data)
print(data.shape)
print(header)


#reader = vtk.vtkNrrdReader()
#reader.SetFileName(filename)
#reader.Update()  

#reader=vtkDataSetReader()
#reader.SetFileName(filename)
#reader.ReadAllVectorsOn()
#reader.ReadAllScalarsOn()
#reader.Update()

#model = reader.GetOutput()
#print(model)


#numpoints = model.GetPointData().GetNumberOfTuples()
#print(numpoints)
#pointdata = model.GetPointData().GetScalars().GetTuple3(6520)
#print(pointdata)





# Read Displacement vector volume
