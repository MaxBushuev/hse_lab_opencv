import argparse
import os

import cv2
import numpy as np

def main(args):
    image = cv2.imread(args.image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_binary = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)[1]

    new_image = np.zeros_like(image_binary)
    new_image[round(new_image.shape[1]*0.2):, :] = image_binary[round(image_binary.shape[1]*0.2):, :]

    # I'm not sure about Hough transform parameters here, I found them out through experiments
    lines = cv2.HoughLines(new_image, 10, np.pi/165, 3700)

    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 2000*(-b))
            y1 = int(y0 + 2000*(a))
            x2 = int(x0 - 2000*(-b))
            y2 = int(y0 - 2000*(a))
            cv2.line(image, (x1, y1), (x2, y2), (0,255,0), 3)

    rho1, theta1 = lines[0][0]
    rho2, theta2 = lines[1][0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)[0]), int(np.round(y0)[0])

    cv2.circle(image, (x0, y0), 5, (0, 0, 255), -1)

    cv2.imwrite("lines.jpg", image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default="road1.png")

    args = parser.parse_args()
    assert os.path.exists(args.image_path), 'Image not found'

    main(args)