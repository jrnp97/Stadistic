import cv2
import os
from matplotlib import pyplot as plt


def plot(img, titles, fig_title="Images"):
    """

    :param img:
    :param titles:
    :param fig_title:
    :return:
    """
    plt.figure(fig_title)
    for k in range(len(img)):
        plt.subplot(2, 3, k + 1), plt.imshow(img[k], 'gray')
        plt.title(titles[k])
        plt.xticks([]), plt.yticks([])
    plt.show()


def binary(img):
    """

    :param img:
    :return:
    """
    ret, binar = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # Make binary invert image (Threshold)
    kernel = cv2.getGaussianKernel(ksize=20, sigma=-1)  # Filter low-pass filter (Gaussian)
    closing = cv2.morphologyEx(binar, cv2.MORPH_CLOSE, kernel)  # Applying closing
    return binar, closing


def save_detections(img, closing, filename, base='/media/pc/Windows/Users/Jaime/PycharmProjects/vision/data/detections'):
    # Get image contours
    _, counters, _ = cv2.findContours(closing, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    print("No. detections = {}".format(len(counters)))
    i = 0
    valid = []
    for count in counters:
        x, y, w, h = cv2.boundingRect(count)  # Get BoundingBox .
        if w > 50 and h > 50:  # Constrain to Valid Bounding Box
            i += 1
            n_img = img[y:y+h, x:x+w]  # Get new images
            # cv2.imwrite(os.path.join(base, '{0}_detection_{1}.png'.format(filename, i)), n_img)
            valid.append(count)
    return valid


def plot_detections(img, valid):
    excludes = []
    for count in valid:
        M = cv2.moments(count)  # Moments of regions
        try:
            cx = int(M['m10'] / M['m00'])  # Get center on x
            cy = int(M['m01'] / M['m00'])  # Get center on y
        except ZeroDivisionError:
            excludes.append(1)
        else:
            center = (cx, cy)  # Build global center
            area = cv2.contourArea(count)  # Get area
            perim = cv2.arcLength(count, True)  # Get perimeter
            # Plot characters
            cv2.putText(img, "A: {0:2.1f}".format(area), center,
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.3, (255, 255, 255), 3)
            cv2.putText(img, "P: {0:2.1f}".format(perim), (cx, cy + 30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.3, (255, 255, 255), 3)

        epsilon = 0.01 * cv2.arcLength(count, True)
        aprox = cv2.approxPolyDP(count, epsilon, True)
        img = cv2.drawContours(img, [aprox], 0, (255, 0, 0), 3)

    print("No. detections excluded = {}".format(len(excludes)))
    plot(img=[img], titles=["Binary contours in image"], fig_title="Detections")


def save_scaling(img, dest, idx):
    """

    :param img:
    :return:
    """
    low_img = cv2.GaussianBlur(img, (5, 5), 0)  # Apply low pass filter
    im_resize = cv2.resize(low_img, (148, 148), interpolation=cv2.INTER_CUBIC)  # Resizing image
    cv2.imwrite(dest + "/{}.png".format(idx), im_resize)  # Save image


"""
    # Show images processed
    titles = ['Original', 'Binary', 'Closing']
    images = [img, binary, closing]
    plot(img=images, titles=titles, fig_title="Morphological Transformations")
"""