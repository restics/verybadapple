import time
from timeit import default_timer as timer
import numpy as np
import cv2
import printToPage

video = cv2.VideoCapture('badapple.mp4')
success, image = video.read()
video_array = []
count = 0


ratio = 52 / image.shape[1]
width = int(image.shape[1] * ratio)
height = int(image.shape[0] * ratio)
dim = (width, height)
print(dim)
page_instance = printToPage.page_wrapper()


"""
Given 2d array of pixels (GRAY), 
returns 2d array of 
⬛ (170 - 255),
⬜ (85 - 170), 
◦ (0 - 85)
number in parentheses is the blue value (first index) of each pixel
essentially, gets the blue value and replaces the entire pixel's array with a single value
"""
def to_black_white(image_array):
    text_array = np.empty((len(image_array), len(image_array[0])))
    text_array = text_array.astype('int')
    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            if image_array[i, j, 0] > 170:
                text_array[i, j] = 4
            elif 170 >= image_array[i, j, 0] > 85:
                text_array[i, j] = 2
            else:
                text_array[i, j] = 0
    return text_array


def print_unicode_image(image_array):
    for x in range(len(image_array)):
        print(''.join(image_array[x]))
    print('\n')



wait = input("start? (press enter)")
while success:
    start = timer()
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    page_instance.display_image(to_black_white(np.asarray(resized_image)), count)
    success, image = video.read()
    count += 1

    end = timer()
    delta_time = end-start
    print(f'frame: {count} time to render: {delta_time}' )
