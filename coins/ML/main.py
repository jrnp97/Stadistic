import os
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

if __name__ == "__main__":

    model = pickle.load(open('finalized_model.sav', 'rb'))

    y_pred = []
    """Predicts images"""

    data = os.path.join(DATA_DIR, 'training')
    for image in os.listdir(data):
        im_matrix = cv2.imread(os.path.join(data, image), 0)
        x_pred = [pixel for column in im_matrix for pixel in column]
        res = model.predict([x_pred])
        y_pred.append(res)
        print("Predict - {} = {}".format(image, res))

    value = sum(y_pred)[0]

    print("Predecir valor = {}".format(value))
