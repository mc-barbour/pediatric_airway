
def transform_convert(tranformSequenceName, referenceVolumeName):
    """
    Function to loop through a transform sequence and convert to a displacement field

    Input: Name of transform sequence, name of reference volume
    """
    transfer_seq = slicer.util.getNode(tranformSequenceName)
    reference_volume = slicer.util.getNode(referenceVolumeName)
    for node_idx in range(transfer_seq.GetNumberOfDataNodes()):
        transfer_node = tfnode.GetNthDataNode(node_idx)
        slicer.modules.transforms.logic().ConvertToGridTransform(transfer_node, refvolume)
    return


def sequence_volume_probe(modelNode, volumeNode_, n_start, n_vol):
    """
    Function to loop through the "ProbeVolumeWithModel" function in Slicer.

    Input: Surface Name, Volume Name Prefix, Image Start, Number of Images
    """
    probe = slicer.modules.probevolumewithmodel
    parameters = {}
    parameters['InputModel'] = slicer.util.getNode(modelNode).GetID()
    for n in range(n_start, n_vol + n_start):
        print("Volume:", n)
        outModel=slicer.vtkMRMLModelNode()
        outModel.SetName("displacement_surf_"+str(n))
        slicer.mrmlScene.AddNode(outModel)
        parameters['InputVolume'] = slicer.util.getNode(volumeNode_+str(n)).GetID()
        parameters['OutputModel'] = outModel.GetID()
        slicer.cli.runSync(probe, None, parameters)
    return


