"""
This scripts make structures from training examples from images.
"""
import cv2
import os
import numpy as np
from sklearn.neural_network import MLPClassifier
import pickle


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

if __name__ == "__main__":
    training_examples = os.path.join(DATA_DIR, 'training_examples')
    x = []
    y = []

    # Make training set
    for image in os.listdir(training_examples):
        im_matrix = cv2.imread(os.path.join(training_examples, image), 0)
        im_vector = [pixel for column in im_matrix for pixel in column]
        x.append(im_vector)
        y.append(int(image.split('_')[0]))

    x = np.array(x)
    y = np.array(y)
    m = len(y)

    model = MLPClassifier(solver='lbfgs', alpha=1e-2)

    model.fit(x, y)
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

