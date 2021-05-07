import sys

import cv2
import glob

from natsort import natsorted

def main():

    print(sys.argv[1])

    #movie_dir = '/Users/mbarbour/Research/Trachea/Patient_Data/4DCT_109/Movie/'
    #outfile = 'xy_motion.mov'
    #fps = 2.5
    movie_dir = str(sys.argv[1])
    outfile = str(sys.argv[2])
    fps = float(sys.argv[3])

    files = natsorted(glob.glob(movie_dir+'*.png'))
    print(files)
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


if __name__ == "__main__":
    main()
