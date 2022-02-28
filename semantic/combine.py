# -*- coding: utf-8 -*-
"""
Created on Wed May 12 12:25:31 2021

@author: ADMANDODE
"""


import numpy as np
import imageio
import matplotlib.pyplot as plt
import glob


def overlay(aimg,pred, colortuple = (22,240,118), alpha=1):
    color = np.ones(aimg.shape)*np.array(colortuple)/255
    overlay_alpha = np.tile(pred*alpha,(3,1,1)).swapaxes(0,2).swapaxes(0,1)
    image_overlay = (aimg.astype('float')/255*(1-overlay_alpha) + color*overlay_alpha)*255
    
    return  image_overlay.astype('uint8')

def pred_out(pred, threshold=0.5):
    
    pred[pred>=threshold] = 1
    pred[pred<threshold] = 0
    
    color = np.ones((pred.shape[0],pred.shape[1],3))*255
    overlay_alpha = np.tile(pred,(3,1,1)).swapaxes(0,2).swapaxes(0,1)
    image_overlay = (color*overlay_alpha)
    return  image_overlay.astype('uint8')



def img_pred(img_path, pred_path, grayimg=False, predcolor=[255,0,0],alpha=1.0, outfolder=None, threshold=None):
    
    # Read original image and prediction 
    img = imageio.imread(img_path)
    pred = imageio.imread(pred_path)

    

    # If threshold, set all above to 1 and rest 0
    if threshold is not None:
        pred = pred_out(pred/255, threshold)[:,:,0]
        
    # if grayimg
    if grayimg:
        gray = img
        c = 0.2989*img[:,:,0] + 0.5870*img[:,:,1] + 0.1140*img[:,:,2]
        for i in range(3):
            gray[:,:,i] = c
        img=gray
    
    # combine image and prediction        
    combined = overlay(img,pred/255,colortuple=predcolor,alpha=1)
    
    # Save combination if foutfolder is given
    if outfolder is not None:
        imgname = img_path.split('\\')[-1]
        imageio.imwrite(outfolder + '\\' + imgname, combined)
        


if __name__ == '__main__':
    
    imagefolder = r"F:\ADRASSO\code\Bjørnar master\color" + '\\'
    predictionfolder = r"F:\ADRASSO\code\Bjørnar master\results\nostats_640x480_rn18" + '\\'
    outfolder = r"F:\ADRASSO\code\Bjørnar master\results\nostats_640x480_rn18_combine" + '\\'
    
    
    imagepaths = glob.glob(imagefolder+'*.jpg')
    
    
    for imagepath in imagepaths:
        pred_name = imagepath.split('\\')[-1].replace('jpg','png')
        
        img_pred(imagepath,predictionfolder+pred_name, outfolder=outfolder)
    
    
    
    

    