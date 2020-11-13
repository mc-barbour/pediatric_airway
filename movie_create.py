import cv2
import glob
from natsort import natsorted

movie_dir = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Movie/'
outfile = 'xy_motion.mov'
fps = 2.5

files = natsorted(glob.glob(movie_dir+'*xy*.png'))

frames_array = []

for i in range(len(files)):
# for i in range(5):
    img = cv2.imread(files[i])

    height, width, layers = img.shape
    size = (width, height)
    frames_array.append(img)

out = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), fps,
 size)

for i in range(len(frames_array)):
    out.write(frames_array[i])

out.release()
