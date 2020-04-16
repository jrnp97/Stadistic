import numpy as np
from matplotlib import pyplot as plt
from lin_reg.functions import get_data, separate, h, j_dev


def g(theta: np.array, x: np.array, n: int, m: int) -> list:
    """
    This function calculate the sigmoid function values.
    :param theta: values of thetas.
    :param x: values of features.
    :param n: number of features.
    :param m: number of training examples.
    :return: array with all values of hypothesis function for each training example.
    """
    if (len(theta) == n) and (len(x) == m):
        return 1 / (1 + np.power(np.e, np.dot(-1, h(theta=theta, x=x, n=n, m=m))))
    else:
        raise TypeError("the theta and x size should be equal to n and m values respectively")


def j(htp: np.array, y: np.array, m: int) -> float:
    """
    This function calculate the CostFunction value of hypothesis function (htp).
    :param htp: hypothesis function values.
    :param y: real values to predict for the model.
    :param m: number of training examples.
    :return: float number equal to cost function of h respect to y.
    """
    return -1 * (sum([((y[i]*np.log(htp[i])) + ((1 - y[i]) * np.log(1 - htp[i]))) for i in range(m)]) / m)


def show(c, t):
    # -- Calculating final cost function -- #
    print("#", "-" * 10, "INFORMATION", "-" * 10, "#")
    print("The CostFunction Init value = {0}".format(c[0]))
    print("The CostFunction Finish value = {0}".format(c[len(c)-1]))
    print("#", "-" * 10, "RESUME", "-" * 10, "#")
    print("Theta values")
    print("-" * 5)
    print(t)


def gradient_descent(x: np.array, y: np.array, theta: list, max_iter: int, m: int, n: int, alpha: float) -> list:
    """
    This function calculate the optima theta values that can be to got with max_iter run gradient descent algorithm
    :param x: array with features values
    :param y: array with real objective value
    :param theta: array with theta initial values
    :param max_iter: number of max iterations for run gradient descent algorithm
    :param m: number of training examples
    :param n: number of features
    :param alpha: learning rate
    :return: python list with the optima theta values got
    """
    # -- Calculating initial cost function -- #
    cost_f = []
    c = j(htp=g(theta, x, n, m),  # Calculating cost with new theta values
               y=y,
               m=m
               )
    cost_f.append(c)
    try:
        for ite in range(max_iter):
            # Calculating hypothesis function values with actual theta values
            htp = g(theta, x, n, m)
            # Make a transpose of x array because this have a size of (m,n)
            x_trans = x.transpose()  # Now have (n,m)
            # Calculating new theta values and save in array temp
            temp = []
            for idx in range(n):
                t = theta[idx] - alpha * (j_dev(htp, y, x_trans[idx], m))
                temp.append(t)

            # Set the new theta values to original array
            for i in range(n):
                theta[i] = temp[i]
            c = j(htp=g(theta, x, n, m),  # Calculating cost with new theta values
                       y=y,
                       m=m
                       )
            cost_f.append(c)
            # plt.plot(cost_f)
            # plt.show()
        else:
            show(cost_f, theta)
    except KeyboardInterrupt or StopIteration:
        show(cost_f, theta)
    # Return theta values
    return theta


def training(data: np.array, m: int, n: int, alpha: float, m_iter: int) -> list:
    """
    This function execute training process with gradient descent algorithm and return theta values calculate
    and normalization parameters for each feature.
    :param data: numpy matrix with all training examples
    :param m: number of training examples
    :param n: number of features
    :param norm: boolean to say if the x values will be normalization
    :param alpha: is the learning rate.
    :param m_iter: number max of iteration for run gradient descent algorithm
    :return: [ python list with theta values, python list with normalization parameters ]
    """

    # --- Separate data on x and y values -- #
    x, y = separate(data, n)

    # -- Calculate theta values -- #
    i_theta = [0 for i in range(n)]  # Set initial theta values
    # Run gradient descent function
    f_theta = gradient_descent(x=x,
                               y=y,
                               theta=i_theta,
                               max_iter=m_iter,
                               m=m,
                               n=n,
                               alpha=alpha
                               )
    return f_theta


def predict(htp: np.array) -> list:
    result = []
    for value in htp:
        if value > 0.5:
            result.append(1)
        else:
            result.append(0)
    return result