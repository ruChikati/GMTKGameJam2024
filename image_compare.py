import os, math, operator
from PIL import Image, ImageChops
from numpy import mean, array

def meandiff(im1, im2):
    dif = ImageChops.difference(im1, im2)
    return mean(array(dif))

def score(artwork, screenshot):
    size = 500, 500
    img1 = Image.open(f"artworks{os.sep}{artwork}").convert('RGB')
    img1.resize(size)
    img2 = Image.open(screenshot)
    img2.resize(size)
    return meandiff(img1.resize(size), img2.resize(size))
