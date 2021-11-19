# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:32:08 2021

@author: marcu
"""

import numpy as np
import matplotlib.pyplot as plt
import skimage.filters as flt
import pandas as pd
import pathlib
import cv2

def find_brightest_area(path_to_image):
    if not path_to_image.exists():
        print("File does not exist")
        return -1
        
    img = cv2.imread( str( path_to_image.resolve() ) )
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Naive method to find brightest pixel     
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(imgGray)
    
    # image, center of circle, radius, color (RGB) - drawing on RGB image, thickness 
    cv2.circle(imgRGB, maxLoc, 5, (255, 0, 0), 2) # draws red circle on the pixel
    
    # robuster   -> Gaussian Blurring , radius (here (::,::) must have two odd numbers (equal) )
    radius = 15
    imgGray_gauss = cv2.GaussianBlur(imgGray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(imgGray)
    cv2.circle(imgRGB, maxLoc, radius, (255, 0, 0), 2) # draws red circle on the pixel
    
    return (imgRGB, maxLoc) # return drawn on pixel along with the center of the Gaussian blurred circle


def display_image_as_histogram(x_dat, y_dat, clean=False):
    # Kaestner code pasted (partially)
    nBins = 100 # Here, we select the number of bins in the histograms.
    H, xedges, nedges = np.histogram2d(x_dat.ravel(), y_dat.ravel(), bins=nBins)   # create 2d histogram -> pixel vals for two images. 
    """
    I think we feed it one picture for the neutrons and one of x-rays -> 2d hist
    """
    nH,nax = np.histogram(y_dat.ravel(),bins=nedges)
    xH,xax= np.histogram(x_dat.ravel(),bins=xedges)    
    
    H = flt.median(H,np.ones([3,3]))
    
    return 0



if __name__ == "__main__":
    
    ## Finding the brightest are on an image -> see example below
    
    test_image = (pathlib.Path.cwd()) / "Maker.jpg"
    test_image, maxLoc = find_brightest_area(test_image)
    
    plt.figure(dpi = 350)
    plt.imshow(test_image)
    
    
