from VA.functions import *


if __name__ == "__main__":
    img_path = '/media/pc/Windows/Users/Jaime/PycharmProjects/vision/data/proof2.jpg'
    img = cv2.imread(img_path, 0)
    detection_path = '/media/pc/Windows/Users/Jaime/PycharmProjects/vision/data/examples'
    bin, closing = binary(img)

    titles = ["original", "binary", "closing"]
    images = [img, bin, closing]

    # plot(images, titles)

    valid = save_detections(img=img, closing=closing, filename='proof', base=detection_path)
    plot_detections(img, valid)
    for idx, img in enumerate(os.listdir(detection_path)):
        im = cv2.imread(os.path.join(detection_path, img), 0)
        save_scaling(img=im, dest='/media/pc/Windows/Users/Jaime/PycharmProjects/vision/data/training', idx=idx)


