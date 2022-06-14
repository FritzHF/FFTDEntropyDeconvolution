import itertools
import time
import numpy as np
from scipy.io import loadmat
from scipy.io import savemat
import sys
from util.deconvolution import Deconvolution

# For use in Matlab-script findLambdaSlider.m;
# Copy of tdematlab without print messages; Uses only 10 frame for deconvolution
def tdematslider():
    # F: Load Testfile from Matlab
    matpath = sys.argv[1]
    matcontent = loadmat(matpath + 'matslider.mat')
    lamb_arr = [np.float64(sys.argv[2])]
    lamb_t_arr =  [np.float64(sys.argv[3])]
    img = matcontent['img']
    pf = matcontent['psf']
        # correct shape if image not quadratic
    if img.ndim == 2:
            if img.shape[0] != img.shape[1]:
                minshape = np.min(img.shape)
                img = img[:minshape, :minshape]
            xdims = img.shape
    else:
             # F : Load Img + PF; For IMG, time is in 3rd dimension, but is needed in 1st
             # F: transpose image to correct format
            img = matcontent['img'].transpose(2, 0, 1)
            if img.shape[1] != img.shape[2]:
                minshape = np.min(img.shape)
                img = img[9:19, :minshape, :minshape]
            else:
                img = img[9:19, :, :]

            xdims = (img.shape[0], img.shape[1])

    # start deconvolution with parameter loops
    eps_arr = matcontent['eps_arr']
    maxit = 1
    startingtime = time.strftime('%Y-%m-%d-%Hh%M', time.localtime(time.time()))
    for lamb_t, lamb, eps in itertools.product(lamb_t_arr, lamb_arr, eps_arr):
        if img.ndim == 2:
            lamb_t = 0.0

        Dec = Deconvolution(pf, img, lamb, lamb_t, eps, maxit)
        result = Dec.deconvolve()

        # Write array into Matlab file to process further
        # Transpose Result to match Matlab format

        savemat(matpath + "matpyslider.mat", mdict ={'result' : result})
        return result

if __name__ == '__main__':
    tdematslider()