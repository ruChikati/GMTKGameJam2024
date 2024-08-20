import io, os, random

import imgcompare, math, operator
from PIL import Image


def score(artwork, screenshot):
    size = 500, 500
    img2 = Image.open(screenshot)
    img2.thumbnail(size, Image.Resampling.LANCZOS)
    img2.save(screenshot, "png")
    img1 = Image.open(f"artworks{os.sep}{artwork}").convert('RGB')
    img1.thumbnail(size, Image.Resampling.LANCZOS)
    img1.save(f"artworks{os.sep}{artwork}", "png")
    return imgcompare.image_diff_percent(img1, img2)
