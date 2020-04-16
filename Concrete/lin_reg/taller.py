import pandas
import numpy as np
from random import sample
from sklearn.metrics import mean_absolute_error
from lin_reg.funtions import training, separate, normalization, h as hypothesis, get_data, mape as mean_absolute_percentage_error

# Define path to found xlsx file with training data
xls_route = "E:\\Desktop\\Manejo de datos\\IA\\Machine Learning\\ex1data2.xlsx"

# Set attributes names to a python list
names = ["x0", "x1", "x2", "y"]

"""
# No normalization on data
--------------------------
# iterations = 1'000.000
# alpha = 0.0000001

# Normalization on data
-----------------------
# iterations = 300.000
# alpha = 0.001
"""


# def run(iterations: int = 1000000, norm: bool = False, alpha: float = 0.0000001) -> float:
def run(iterations: int = 500000, norm: bool = True, alpha: float = 0.001) -> float:

    # -------- INIT TRAINING SECTION -------- #
    # Read training set information
    training_set = pandas.read_excel(xls_route, names=names)

    # -- Set training information -- #
    length = len(training_set.y.values)
    m = round(length * 0.6)  # Number of training examples
    n = len(training_set.keys()) - 1  # Number of features
    t_index = sample(range(length), m)  # Generate m numbers between 1 and length
    # t_index = list(range(0, m))

    # -- Short data -- #
    training_data, real_data = get_data(training_set.values, t_index)

    # -- Training data -- #
    theta, n_params = training(data=training_data, m=m, n=n, m_iter=iterations, norm=norm, alpha=alpha)
    # -------- END TRAINING SECTION -------- #

    # -------- INIT VERIFY SECTION -------- #
    # -- Validate data -- #
    m = round(length * 0.4)  # Recalculate m for validate data
    x, y = separate(real_data, n)  # Separate data on x and y values
    if norm:
        # - Normalizing x values - #
        x_temp = []
        x_trans = x.transpose()
        x_temp.append(x_trans[0])  # Exclude x0's values of normalization process
        for idx in range(1, n):
            x_val, p = normalization(x_trans[idx], n_params[idx - 1])
            x_temp.append(x_val)
        x = np.array(x_temp).transpose()

    # - Calculating hypothesis function values - #
    htp = hypothesis(theta=theta, x=x, n=n, m=m)

    # - Calculating MAPE value - #
    e = mean_absolute_error(y_true=y, y_pred=htp)
    error = mean_absolute_percentage_error(y_true=y, y_pred=htp)

    print("#", "-" * 10)
    print("The Mean Absolute Percentage Error is {0} %".format(error))
    print("#", "-" * 28, "#")
    # -------- END VERIFY SECTION -------- #

    for i in range(m):
        print("y = {0} :: h = {1} -> diff = {2}".format(y[i], htp[i], np.abs(htp[i]-y[i])))

    return error


if __name__ == "__main__":
    run()