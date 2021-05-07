import numpy as np
from vtk import *
from read_vtk import *
import glob
from natsort import natsorted
import plotly.graph_objects as go
import plotly.express as px


#Create tube around line
line = vtk.vtkLineSource()
line.SetPoint1(1.0,0.0,0.0)
line.SetPoint1(0.0,1.0,0.0)

tubeFilter=vtk.vtkTubeFilter()
tubeFilter.SetInputConnection(line.GetOutputPort())
tubeFilter.SetRadius(0.025)
tubeFilter.SetNumberOfSides(50)
tubeFilter.Update()

