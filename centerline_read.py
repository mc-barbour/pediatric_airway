import os
import sys

import numpy as np

def main():

    centerline_file = sys.argv[1]
    file_prefix = os.path.splitext(os.path.split(centerline_file)[1])[0]

    x = np.genfromtxt(centerline_file, skip_header=1, usecols=0)
    y = np.genfromtxt(centerline_file, skip_header=1, usecols=1)
    z = np.genfromtxt(centerline_file, skip_header=1, usecols=2)

    target_num_points = 100
    skip = int(len(x)/target_num_points)

    print(skip, len(x[::skip]))

    filename = file_prefix+'.csv'
    print(filename)

    np.savetxt(filename, np.array([x[::skip], y[::skip], z[::skip]]).T, delimiter=',')



if __name__ == "__main__":
    main()
