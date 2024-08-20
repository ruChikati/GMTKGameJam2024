import os
from imgcompare import image_diff_percent
from PIL import Image


def score(artwork, screenshot):
    size = 500, 500
    img1 = Image.open(f"artworks{os.sep}{artwork}").convert('RGB')
    img1.resize(size)
    img2 = Image.open(screenshot)
    img2.resize(size)
    return image_diff_percent(img1.resize(size), img2.resize(size))
