
def transform_convert(tranformSequenceName, referenceVolumeName):
    """
    Function to loop through a transform sequence and convert to a displacement field

    Input: Name of transform sequence, name of reference volume

    Example Usage: transform_convert("Transform_name", "Input_volume_name")
    """
    transfer_seq = slicer.util.getNode(tranformSequenceName)
    reference_volume = slicer.util.getNode(referenceVolumeName)
    for node_idx in range(transfer_seq.GetNumberOfDataNodes()):
        transfer_node = transfer_seq.GetNthDataNode(node_idx)
        slicer.modules.transforms.logic().ConvertToGridTransform(transfer_node, reference_volume)
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
        outModel.SetName("displacement_field_"+str(n))
        slicer.mrmlScene.AddNode(outModel)
        parameters['InputVolume'] = slicer.util.getNode(volumeNode_+str(n)).GetID()
        parameters['OutputModel'] = outModel.GetID()
        slicer.cli.runSync(probe, None, parameters)
    return

def findBrowserForSequence(sequenceNode):
    browserNodes = slicer.util.getNodesByClass("vtkMRMLSequenceBrowserNode")
    for browserNode in browserNodes:
        if browserNode.IsSynchronizedSequenceNode(sequenceNode, True):
            return browserNode
        return None



def laplacian_sharp_seq(input_seq_name, n_start, n_vol):
    """
    Function to loop perform laplacian filter on sequece of images in slicer
    """
    # set up sequence widget (not a module)
    
    # filter_widget = slicer.modules.SimpleFiltersWidget
    # filter_params = filter_widget.filterParameters
    
    # seq = slicer.util.getNode(input_seq_name)
    # seq_browser = slicer.util.getNode("Sequence browser")
    # filter_widget.filterSelector.setCurrentIndex(142)
    
    # filter_params.input = seq
    
    # b = filter_widget.applyButton
    
    for node_id in range(n_start, n_vol + n_start):
        print(node_id)
        # set display node
        seq_browser.SetSelectedItemNumber(node_id)
        
        # set output volume
        outModel=slicer.vtkMRMLScalarVolumeNode()
        outModel.SetName("test_py_"+str(node_id))
        slicer.mrmlScene.AddNode(outModel)
        filter_params.output = outModel
        b.clicked()
    return
        # set input volume
        # vol=seq.GetDisplayNode()

        # b.enabled=True
        
        b.clicked()
    return

#%%
   
    


#%%

# define filter Widget    
filter_widget = slicer.modules.SimpleFiltersWidget
filter_params = filter_widget.filterParameters
filter_widget.filterSelector.setCurrentIndex(142)
b = filter_widget.applyButton    

# load sequence and browser
seq = slicer.util.getNode("Sequence")
seq_browser = slicer.util.getNode("Sequence browser")


def update_display(node):
    
    app_logic = slicer.app.applicationLogic()
    selection_node = app_logic.GetSelectionNode()
    selection_node.SetReferenceActiveLabelVolumeID(node.GetID())
    app_logic.PropagateVolumeSelection(0)
    return None


def laplace_sharp_function(seq_name, n_start, n_vol):
    import time
    # define widget
    filter_widget = slicer.modules.SimpleFiltersWidget
    filter_params = filter_widget.filterParameters
    filter_widget.filterSelector.setCurrentIndex(142)
    b = filter_widget.applyButton
    
    # load sequence and sequence browser
    seq = slicer.util.getNode(seq_name)
    seq_browser = slicer.util.getNode(seq_name + " browser")
    
    
    for node_id in range(n_start, n_vol + n_start):
        print(node_id)
        # update_display(seq)
        seq_browser.SetSelectedItemNumber(node_id)
        outModel=slicer.vtkMRMLScalarVolumeNode()
        outModel.SetName("test_py_"+str(node_id))
        slicer.mrmlScene.AddNode(outModel)
        filter_params.outputSelector.setCurrentNode(outModel)
        
        b.clicked()
        print(filter_widget.currentStatusLabel.text)
        time.sleep(10)
        print(filter_widget.currentStatusLabel.text)
    return





#%%
def laplacian_sharp_seq2(input_seq_name, n_start, n_vol):
    """
    Function to loop perform laplacian filter on sequece of images in slicer
    """
    # set up sequence widget (not a module)
    
    filter_widget = slicer.modules.SimpleFiltersWidget
    filter_params = filter_widget.filterParameters
    
    seq = slicer.util.getNode("Sequence")
    # seq_browser = slicer.util.getNode("Sequence browser")
    # filter_widget.filterSelector.setCurrentIndex(142)
    
    for node_id in range(n_start, n_vol + n_start):
        print(node_id)
        # set display node
        # seq_browser.SetSelectedItemNumber(node_id)
        
        # set output volume
        outModel=slicer.vtkMRMLScalarVolumeNode()
        outModel.SetName("test_py2_"+str(node_id))
        slicer.mrmlScene.AddNode(outModel)
        filter_params.output = outModel
        
        # set input volume
        vol=seq.GetNthDataNode(node_id)
        print(vol)
        filter_params.input = vol
    
        b = filter_widget.applyButton
        b.enabled=True
        b.clicked()
    return

def updateOutput(node):
    
    app_logic = slicer.app.applicationLogic()
    selection_node = app_logic.GetSelectionNode()
    selection_node.SetReferenceActiveLabelVolumeID(node.GetID())
    app_logic.PropagateVolumeSelection(0)
    return None


#%%

# Find corresponding sequence browser node
browserNode = slicer.modules.sequences.logic().GetFirstBrowserNodeForSequenceNode(sequenceNode)

# Print sequence information
print("Number of items in the sequence: {0}".format(browserNode.GetNumberOfItems()))
print("Index name: {0}".format(browserNode.GetMasterSequenceNode().GetIndexName()))

# Jump to a selected sequence item
browserNode.SetSelectedItemNumber(5)


