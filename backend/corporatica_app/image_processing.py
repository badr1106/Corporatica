import cv2
import numpy as np
from skimage.segmentation import slic, quickshift, felzenszwalb

def generate_color_histogram(image_path, bins=256):
    image = cv2.imread(image_path)
    hist = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist.tolist()

def generate_segmentation_mask(image_path, algorithm='slic', **params):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if algorithm == 'slic':
        segments = slic(image_rgb, **params)
    elif algorithm == 'quickshift':
        segments = quickshift(image_rgb, **params)
    elif algorithm == 'felzenszwalb':
        segments = felzenszwalb(image_rgb, **params)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    for i in range(np.max(segments) + 1):
        mask[segments == i] = np.random.randint(0, 256)

    return mask