import itertools
import time
import numpy as np
from scipy.io import loadmat
from scipy.io import savemat
import sys
from util.deconvolution import Deconvolution

# For use in Matlab-script postprocessing.m; Tries to only get necessary modules for lighter binary
# Needs the path to the directionary of used .mat file
def tdematlab():
    # Load Matfile from Matlab
    matpath = sys.argv[1]
    matcontent = loadmat(matpath + 'matcontent.mat')
    # Load Img + PF; For IMG, time is in 3rd dimension, but is needed in 1st
    # transpose image to correct format
    img = matcontent['img'].transpose(2,0,1)
    pf = matcontent['psf']
        # correct shape if image not quadratic
    if img.ndim == 2:
            if img.shape[0] != img.shape[1]:
                minshape = np.min(img.shape)
                img = img[:minshape, :minshape]
            xdims = img.shape
    else:
            if img.shape[1] != img.shape[2]:
                minshape = np.min(img.shape)
                img = img[:, :minshape, :minshape]

            xdims = (img.shape[1], img.shape[2])


    #start deconvolution with parameter loops
    lamb_t_arr = matcontent['lamb_t_arr']
    lamb_arr = matcontent['lamb_arr']
    # lamb_t_arr = [0.3, 0.5]
    # lamb_arr = [0.3, 0.5]
    eps_arr = matcontent['eps_arr']
    maxit = 1
    #delta = decon_data['delta']
    #tol = 1e-6
    startingtime = time.strftime('%Y-%m-%d-%Hh%M', time.localtime(time.time()))
    counter = 1
    mat_dict = {}
    for lamb_t, lamb, eps in itertools.product(lamb_t_arr, lamb_arr, eps_arr):
        if img.ndim == 2:
            lamb_t = 0.0
        start = time.time()
        start_hr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
        print("....................................")
        print(".... starting time : ", start_hr ," .......")
        print("deconvolving image ")
        print("lamb_t = ", lamb_t, "  lamb = ", lamb, "  eps = ", eps)
        print(".......starting deconvolution.......")
        Dec = Deconvolution(pf, img, lamb, lamb_t, eps, maxit)
        result = Dec.deconvolve()
        print(".......deconvolution finished.......")
        if result.ndim == 3:
            result = result.transpose(1,2,0)
        mat_dict['result_' + str(counter)] = result
        mat_dict["lamb_" + str(counter)] = lamb
        mat_dict["lamb_t_" + str(counter)] = lamb_t
        counter += 1
        finish = time.time()
        finish_hr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))
        print(".... finished at : ", finish_hr ," .......")
        totaltime = finish-start
        print("total time for deconvolution: ", "{:6.2f}".format(totaltime), " s")
        print("............................")
    print(".........saving to mat file.........")
    mat_dict["keys"] = list(mat_dict.keys())
    savemat(matpath + "matpycontent.mat", mdict=mat_dict)

if __name__ == '__main__':
    tdematlab()