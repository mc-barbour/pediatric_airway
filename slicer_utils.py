
def transform_convert():

    transfer_seq = slicer.util.getNode('OutputTransforms')

    reference_volume = slicer.util.getNode('Pt109_cropped_MultiVolume')

    for node_idx in range(transfer_seq.GetNumberOfDataNodes()):

        transfer_node = tfnode.GetNthDataNode(node_idx)

        slicer.modules.transforms.logic().ConvertToGridTransform(tf_19, refvolume)

    return


def transform_convert():

 transfer_seq = slicer.util.getNode('OutputTransforms')

 reference_volume = slicer.util.getNode('Pt109_cropped_MultiVolume')

 for node_idx in range(transfer_seq.GetNumberOfDataNodes()):

  transfer_node = tfnode.GetNthDataNode(node_idx)

  slicer.modules.transforms.logic().ConvertToGridTransform(tf_19, refvolume)

 return

 def transform_convert():
...  transfer_seq = slicer.util.getNode('OutputTransforms')
...  reference_volume = slicer.util.getNode('Pt109_cropped_MultiVolume')
...  for node_idx in range(transfer_seq.GetNumberOfDataNodes()):
...   transfer_node = transfer_seqan.GetNthDataNode(node_idx)
...   slicer.modules.transforms.logic().ConvertToGridTransform(transfer_node, reference_volume)
...  return

