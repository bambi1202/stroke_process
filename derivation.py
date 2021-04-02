import numpy as np
import cv2
from skimage import color
import matplotlib.pyplot as plt
import imageio

img = cv2.imread("temp/query_img.png")
img = color.rgb2gray(img)
x , y = np.gradient(img)  
xx , xy = np.gradient(x)
yx , yy = np.gradient(y)

Iup =  (1 + np.square(x))*yy - 2*x*y*xy + (1 + np.square(y))*xx
Idown = np.power((2*(1 + np.square(x) + np.square(y))),3/2)
    
final = Iup/Idown
final = abs(final)
# print(final.max())
final = (final - final.min())/(final.max() - final.min())
final = final * 255
final = final.astype(np.uint8)
plt.imshow(final)
imageio.imwrite("figure.jpg", final)
