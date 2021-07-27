import cv2
from PIL import Image, ImageEnhance, ImageOps,ImageDraw

import numpy as np
import os
import sys

folder = sys.argv[1]

header = cv2.imread(f"{folder}/header.png")
footer = cv2.imread(f"{folder}/footer.png")

header_height,header_width,header_columns = header.shape
width = header_width

screenshots = [i for i in os.listdir(folder) if i[:i.find(".")].isdigit()]

if screenshots and not os.path.isdir(f"{folder}/processed"):
    os.mkdir(f"{folder}/processed")

def find_lines(img,top,bottom):
    im = cv2.Laplacian(img,cv2.CV_64F)
    
    for i in range(top,bottom):
        for j in range(im.shape[1]):
                for k in range(im.shape[2]):
                        im[i,j,k] = 255 if im[i,j,k] > 0 else 0
    whites = [i for i in range(im.shape[0]) if (im[i,580] == np.array([255,255,255])).all()]
    
    return [whites[i]+1 for i in range(1,len(whites)) if whites[i] - whites[i-1] > 1] 



for index,file in enumerate(screenshots):
    if int(file[:file.index(".")]) > 0:
        cv2_img = cv2.imread(f"{folder}/{file}")
        pil_img = Image.open(f"{folder}/{file}")

        header_result = cv2.matchTemplate(cv2_img,header,cv2.TM_CCOEFF_NORMED)
        footer_result = cv2.matchTemplate(cv2_img,footer,cv2.TM_CCOEFF_NORMED)

        up,left = np.unravel_index(header_result.argmax(),header_result.shape)
        footer_coordinates = np.unravel_index(footer_result.argmax(),footer_result.shape)
        up += header_height
        height = footer_coordinates[0] - up

        cropped_img = pil_img.crop((left,up,left+width,up+height))
        bnw_img = ImageOps.grayscale(cropped_img)
        enhancer = ImageEnhance.Contrast(bnw_img)
        bnw_img = enhancer.enhance(5)
        draw = ImageDraw.Draw(bnw_img)
        
        for i in find_lines(cv2_img,up-10,up+height):
            draw.line((0,i-up) + (width,i-up),fill=128)

        bnw_img.save(f"{folder}/processed/{int(file[:file.index('.')]):03d}.png")

