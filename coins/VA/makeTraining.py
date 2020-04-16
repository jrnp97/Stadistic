import cv2
import os

from VA.functions import *


if __name__ == "__main__":
    base_path = "/media/pc/Windows/Users/Jaime/PycharmProjects/vision/data/"

    photos = os.path.join(base_path, 'photos')
    """1. Get detections
    for img in os.listdir(photos):
        filename = img.split('.')[0]
        img = cv2.imread(os.path.join(photos, img), 0)  # Get image
        img_binary = binary(img)
        save_detections(img, img_binary, filename)"""

    """2. Preparing Training examples"""
    # 2. Scaling image to a 148 x 148 image
    src = os.path.join(base_path, "detections")
    dest = os.path.join(base_path, "training_examples")
    width = []
    height = []
    for idx, img in enumerate(os.listdir(src)):
        filepath = os.path.join(src, img)
        img = cv2.imread(filepath)  # Get image
        save_scaling(img, dest, idx)



