import pandas
import numpy as np
from random import sample
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from funtions import training, separate, normalization, h as hypothesis, get_data, mean_absolute_percentage_error

# Define path to found xlsx file with training data
xls_route = "E:\\Desktop\\Manejo de datos\\IA\\Machine Learning\\concrete_data.xlsx"

# Set attributes names to a python list
names = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "y"]


def run(iterations: int = 10000) -> float:
    # -------- INIT TRAINING SECTION -------- #
    # Read training set information
    training_set = pandas.read_excel(xls_route, names=names)

    # -- Set training information -- #
    length = len(training_set.y.values)
    m = int(length * 0.6)  # Number of training examples
    n = len(training_set.keys()) - 1  # Number of features
    t_index = sample(range(m + n + 1), m)  # Generate m numbers between 1 and

    # -- Short data -- #
    training_data, real_data = get_data(training_set.values, t_index)
    
    # -- Training data -- #
    theta, n_params = training(data=training_data, m=m, n=n, m_iter=iterations)  # Send data to training
    # -------- END TRAINING SECTION -------- #

    # -------- INIT VERIFY SECTION -------- #
    # -- Validate data -- #
    m = int(length * 0.4)  # Recalculate m for validate data
    x, y = separate(real_data, n)  # Separate data on x and y values
    # - Normalizing x values - #
    x_temp = []
    x_trans = x.transpose()
    x_temp.append(x_trans[0])  # Exclude x0's values of normalization process
    for idx in range(1, n):
        x, p = normalization(x_trans[idx], n_params[idx - 1])
        x_temp.append(x)
    x_norm = np.array(x_temp).transpose()

    # - Calculating hypothesis function values - #
    htp = hypothesis(theta=theta,
                     x=x_norm,
                     n=n,
                     m=m
                     )

    # - Calculating MAPE value - #
    error2 = mean_absolute_error(y_true=y, y_pred=htp)
    error = mean_absolute_percentage_error(y_true=y, y_pred=htp)

    print("#", "-" * 10)
    print("The Mean Absolute Percentage Error is {0} - {1}".format(error, error2))
    print("#", "-" * 28, "#")

    # -------- END VERIFY SECTION -------- #
    return error2


if __name__ == "__main__":
    run()