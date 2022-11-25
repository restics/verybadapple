import cv2
import os
import numpy as np
import re

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
w = 1920
h = 923
directory = 'images\\'


def sort_images(list):
    for i in range(1,list.size):
        list[i] = f'frame{i}.png'

    return list

out = cv2.VideoWriter('video.mp4', fourcc, 30, (w, h), isColor=True)

count = 0
imglist = np.array(os.listdir('images'))
imglist = sort_images(imglist)

for img in imglist:
    try:
        print (directory + img)
        img = cv2.imread(directory + img)
    except Exception as e:
        print(e)
    img = cv2.resize(img, (w, h))
    out.write(img)
    
    count = count + 1
    print (count)

out.release()


