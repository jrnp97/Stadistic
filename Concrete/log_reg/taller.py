import pandas
import numpy as np
from random import sample
from sklearn.metrics import mean_absolute_error
from log_reg.functions import g, get_data, training, separate, predict

# Define path to found xlsx file with training data
xls_route = "E:\\Desktop\\Manejo de datos\\IA\Machine Learning\\log_reg\\Libro1.xlsx"

# Set attributes names to a python list
names = ["x0", "x1", "x2", "y"]


def run(iterations: int = 10000, alpha: float = 0.001) -> float:
    # -------- INIT TRAINING SECTION -------- #
    # Read training set information
    training_set = pandas.read_excel(xls_route, names=names)

    # -- Set training information -- #
    length = len(training_set.y.values)
    m = round(length * 0.6)  # Number of training examples
    n = len(training_set.keys()) - 1  # Number of features
    t_index = sample(range(length), m)  # Generate m numbers between 1 and length

    # -- Short data -- #
    training_data, real_data = get_data(training_set.values, t_index)

    # -- Training data -- #
    theta = training(data=training_data, m=m, n=n, alpha=alpha, m_iter=iterations)
    # -------- END TRAINING SECTION -------- #

    # -------- INIT VERIFY SECTION -------- #
    # -- Validate data -- #
    m = round(length * 0.4)  # Recalculate m for validate data
    x, y = separate(real_data, n)  # Separate data on x and y values

    # - Calculating hypothesis function values - #
    htp = g(theta=theta, x=x, n=n, m=m)
    y_pred = predict(htp)

    print("#", "-" * 10)
    print("The Mean Absolute Error is {0} %".format(mean_absolute_error(y, y_pred)))
    print("#", "-" * 28, "#")
    for real, pred in zip(y, y_pred):
        print("y = {0} - h = {1}".format(real, pred))
    # -------- END VERIFY SECTION -------- #
    return 0.0


if __name__ == "__main__":
    run()
