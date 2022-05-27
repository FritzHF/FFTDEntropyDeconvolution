import itertools
import skimage
import tifffile as tf
import json
import os
import time
import numpy as np
import scipy.io
import util.inputoutput as io
import os
from psf.psf import PSF
from util.deconvolution import Deconvolution

from util.helper import convert_to_uint, convert_to_float

# For use in Matlab-script findLambdaSlider.m;
# Copy of ffmain without print messages; Uses only 1 frame for deconvolution
def ffmain():
    #read in parameters
    # FF: Deprecated for Matlab-input
    # with open('parameters.json', 'r') as read_file:
    #      parameters = json.load(read_file)
    # # psf_data = parameters['psf']
    # io_data = parameters['io']
    # decon_data = parameters['deconvolution']
    #
    # create folders to save results
    # try:
    #     if io_data['read_folder']:
    #         readpaths, savepaths = io.inputoutput_folder(io_data['save_path'], io_data['read_path'],
    #                                                      io_data['create_image_folder'])
    #     else:
    #         read_image_path, save_image_path = io.inputoutput(io_data['save_path'],
    #                                                           io_data['read_path'],
    #                                                           io_data['image_name'],
    #                                                           io_data['create_image_folder'])
    #         readpaths = [read_image_path]
    #         savepaths = [save_image_path]
    # except Exception as E:
    #     print(E)
    #     return

    # for read_image_path, save_image_path in zip(readpaths, savepaths):
    #     try:
    #         img = tf.imread(read_image_path)
    #     except Exception as E:
    #         print(E)
    #         print("!! Failed to read image "+read_image_path)
    #         continue
    # F: Load Testfile from Matlab
    matpath = sys.argv[1]
    #matpath = "/home/fforster/Code/CalciumSignaling/"
    matcontent = scipy.io.loadmat(matpath + 'matslider.mat')
    lambd = np.float64(sys.argv[2])
    #lambd = np.float64(0.500000000000000)
    lamb_arr = [lambd]
    # F : Load Img + PF; For IMG, time is in 3rd dimension, but is needed in 1st
    # F: transpose image to correct format
    img = matcontent['img']
    pf = matcontent['psf']
        # correct shape if image not quadratic
    if img.ndim == 2:
            if img.shape[0] != img.shape[1]:
                minshape = np.min(img.shape)
                img = img[:minshape, :minshape]
            xdims = img.shape
    else:
            img = matcontent['img'].transpose(2, 0, 1)
            if img.shape[1] != img.shape[2]:
                minshape = np.min(img.shape)
                img = img[9, :minshape, :minshape]
            else:
                img = img[9, :, :]

            xdims = (img.shape[0], img.shape[1])

        # load or create point spread function
        # F: Deprecated for Matlabscript
        # if psf_data['experimental']:
        #     psf = tf.imread(psf_data['location'])
        #     pf = PSF(xdims)
        #     pf.data = psf
        # else:
        #     psf_data['xysize'] = xdims[0]
        #     pf = PSF(xdims, **psf_data)

    # start deconvolution with parameter loops
    lamb_t_arr = lamb_arr
    eps_arr = matcontent['eps_arr']
    # lamb_t_arr = [0.5]
    # lamb_arr = [0.5]
    # eps_arr = [0.0001]
    maxit = 1
    #delta = decon_data['delta']
    #tol = 1e-6
    startingtime = time.strftime('%Y-%m-%d-%Hh%M', time.localtime(time.time()))
    #with open(save_image_path+'parameters_'+startingtime+'.json', 'w') as outfile:
       # json.dump(parameters, outfile)
    for lamb_t, lamb, eps in itertools.product(lamb_t_arr, lamb_arr, eps_arr):
        if lamb_t != 0.0 and lamb_t != lamb:
            continue
        if img.ndim == 2:
            lamb_t = 0.0

        #            imf = convert_to_float(img)
        Dec = Deconvolution(pf, img, lamb, lamb_t, eps, maxit)
        result = Dec.deconvolve()
        #T, X, Y = result.shape
        # if original image is 2D only, a dimension needs to be dropped
        #if T == 1:
        #    result = result[0]
        # save result
        io.set_baseline(img, result)
        #            imu = convert_to_uint(result)
        #result = result.astype(np.uint16)
        #F Deprecated for Matlab
        # tf.imwrite(io.create_filename_decon(save_image_path, lamb, lamb_t, maxit, eps),
        #            result, photometric='minisblack')
        # #F: Test save original img
        # tf.imwrite(io.create_filename_decon(save_image_path + 'orig', lamb, lamb_t, maxit, eps),
        #            img, photometric='minisblack')
        # Write array into Matlab file to process further
        # Transpose Result to match Matlab format

        scipy.io.savemat(matpath + "matpyslider.mat", mdict ={'result' : result})
        return result

#if __name__ == '__main__':
    #main()
ffmain()