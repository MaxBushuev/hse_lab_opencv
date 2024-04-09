import argparse
import os

import cv2
import numpy as np

def main(args):
    image = cv2.imread(args.image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_binary = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY_INV)[1]

    contours, _ = cv2.findContours(image_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    widths = []
    heights = []
    for contour in contours:
        _, _, width, height = cv2.boundingRect(contour)

        widths.append(width)
        heights.append(height)

    print(f"Number of symbols: {len(contours)}, median width: {np.median(widths)}, median height: {np.median(heights)}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default="chars1.png")

    args = parser.parse_args()
    assert os.path.exists(args.image_path), 'Image not found'

    main(args)