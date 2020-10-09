Python 3.6.7 (default, Sep 29 2020, 23:06:45) 
[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.5)] on darwin
>>> slicer.modules.ProbeVolumeWithModel()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'ProbeVolumeWithModel'
>>> slicer.modules.ProbeVolumeWithModel
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'ProbeVolumeWithModel'
>>> slicer.modules
<module 'modules' from '/Applications/Slicer 2.app/Contents/bin/Python/slicer/__init__.py'>
>>> print(slicer.modules)
<module 'modules' from '/Applications/Slicer 2.app/Contents/bin/Python/slicer/__init__.py'>
>>> print(slicer.modules.list)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'list'
>>> slicer.modules.Transform
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'Transform'
>>> slicer.modules.DataProbeInstance
<DataProbe.DataProbe object at 0x1456368d0>
>>> slicer.modules.ProbeVolume
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'ProbeVolume'
>>> slicer.modules.sampledata
qSlicerScriptedLoadableModule (qSlicerScriptedLoadableModule at: 0x600000cba460)
>>> slicer.modules.probevolume
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'modules' has no attribute 'probevolume'
>>> slicer.modules.probevolumewithmodel
qSlicerCLIModule (qSlicerCLIModule at: 0x600000c28ae0)
>>> slicer.modules.probevolumewithmodel()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: 'qSlicerCLIModule' object is not callable
>>> slicer.modules.probevolumewithmodel
qSlicerCLIModule (qSlicerCLIModule at: 0x600000c28ae0)
>>> ls
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'ls' is not defined
>>> node=getNode('Displacement Field_2')
>>> parameters={}
>>> parameters["InputVolume"]='Displacement Field_3'
>>> parameters["InputModel"] = 'sdf'
>>> parameters["InputModel"] = 'Airway_full_Tube'
>>> parameters["Output Model_3"] = "test"
>>> probe=slicer.modules.probevolumewithmodel
>>> slicer.cli.runSync(probe,None,parameters)
(MRMLCLIPython.vtkMRMLCommandLineModuleNode)0x14acb02e8
>>> 
>>> 
>>> testnode=slicer.cli.runSync(probe,None,parameters)
>>> 
>>> parameters["InputVolume"]=node.GetID()
>>> surf=getNode("Airway_full_Tube")
>>> parameters["InputModel"]=surf.GetID()
>>> outModel=slicer.vtkMRMLModelNode()
>>> slicer.mrmlScene.AddNode(outModel)
(MRMLCorePython.vtkMRMLModelNode)0x14acb0ee8
>>>   parameters["OutputGeometry"] = outModel.GetID()
  File "<console>", line 1
    parameters["OutputGeometry"] = outModel.GetID()
    ^
IndentationError: unexpected indent
>>> parameters["OutputGeometry"] = outModel.GetID()
>>> 
>>> 
>>> parameters["OutputModel"] = outModel.GetID()
>>> slicer.cli.runSync(probe,None,parameters)
(MRMLCLIPython.vtkMRMLCommandLineModuleNode)0x14acb0528