import numpy as np
import nrrd

displacement = nrrd.read_data('Pt109 Displacement Field.nrrd')

print(displacement)

image = nrrd.read('Pt109_TransformedVolumes_1_12 frame1.nrrd')

print(image)


