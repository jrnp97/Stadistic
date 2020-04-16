import numpy as np


def mape(y_true: np.array, y_pred: np.array) -> float:
    """
    Funtion that calculate the MAPE (Mean Absolute Percentage Error).
    :param y_true: real values to predict for the model.
    :param y_pred: values predicted for the model.
    :return: float number.
    """
    if len(y_true) == len(y_pred):
        return float(np.mean((np.abs(y_true - y_pred) / y_true)) * 100)
    else:
        raise TypeError("the y_true and y_pred size should be equals")


def h(theta: np.array, x: np.array, n: int, m: int) -> list:
    """
    This function calculate the hypothesis function values.
    :param theta: values of thetas.
    :param x: values of features.
    :param n: number of features.
    :param m: number of training examples.
    :return: array with all values of hypothesis function for each training example.
    """
    if (len(theta) == n) and (len(x) == m):
        return [sum(theta * x[i]) for i in range(m)]  # Calculating and return all m values of h function.
    else:
        raise TypeError("the theta and x size should be equal to n and m values respectively")


def j_dev(htp: np.array, y: np.array, x: np.array, m: int) -> float:
    """
    This function calculate the CostFunction derivative.
    :param htp: hypothesis function values.
    :param y: real values to predict for the model.
    :param x: features values.
    :param m: number of training examples.
    :return: float equal to CostFunction derivative.
    """
    if len(y) == len(htp):
        return (sum([(htp[i] - y[i]) * x[i] for i in range(m)])) / m
    else:
        raise TypeError("The h and y size should be equal")


def j(htp: np.array, y: np.array, m: int) -> float:
    """
    This function calculate the CostFunction value of hypothesis function (htp).
    :param htp: hypothesis function values.
    :param y: real values to predict for the model.
    :param m: number of training examples.
    :return: float number equal to cost function of h respect to y.
    """
    return (sum([(htp[i] - y[i])**2 for i in range(m)])) / (2*m)


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
    """
    # -- Calculating initial cost function -- #
    cost_i = j(htp=h(theta, x, n, m),  # Calculating cost with new theta values
               y=y,
               m=m
               )
    cost_f = None
    """
    for ite in range(max_iter):
        # Calculating hypothesis function values with actual theta values
        htp = h(theta, x, n, m)
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

    """
        # print("The cost function value for #{0} theta values is {1}".format(ite+2, cost_f))
    # -- Calculating final cost function -- #
    cost_f = j(htp=h(theta, x, n, m),  # Calculating cost with new theta values
               y=y,
               m=m
               )
    print("The CostFunction Init value = {0}".format(cost_i))
    print("The CostFunction Finish value = {0}".format(cost_f))
    print("-" * 10)
    print("-"*10)
    dif = cost_i - cost_f
    por = int((dif/cost_i) * 100)
    print("Difference = {0}".format(dif))
    print("Reduction percentage = {0}%".format(por))
    """
    print("#", "-" * 10, "RESUME", "-" * 10, "#")
    print("Theta values")
    print("-" * 5)
    print(theta)
    # Return theta values
    return theta


def normalization(x: np.array, params: dict = None) -> [np.array, list]:
    """
    This function normalize all x data in the array
    :param x: numpy array with all x in the training examples
    :param params: python dict that is used when the normalization process have the params
    :return: [numpy list with all x data normalize, list with all normalization params ]
    """
    if params is None:
        # Make params dictionary
        p = dict({'mean': np.mean(x), 'max': max(x), 'min': min(x)})
        # Normalizing x values
        value = (x - p['mean']) / (p['max'] - p['min'])
        # Return list
        return [value, p]
    else:
        # Normalizing x values with normalization params defined
        return [(x - params['mean']) / (params['max'] - params['min']), None]


def separate(data: np.array, n) -> [list, list]:
    x = []
    y = []
    for values in data:
        x.append(values[:-(len(values)-n)])
        y.append(values[n])
    return [np.array(x), np.array(y)]


def get_data(d: np.array, idx: list) -> [list, list]:
    t = []
    r = []
    for index in idx:
        t.append(d[index])

    for i in range(len(d)):
        if i not in idx:
            r.append(d[i])
    return t, r


def training(data: np.array, m: int, n: int, norm: bool, alpha: float, m_iter: int) -> [list, list]:
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
    norm_p = None
    if norm:
        # -- Normalizing x values -- #
        x_temp = []
        norm_p = []
        x_temp.append(x.transpose()[0])  # Exclude x0's values of normalization process
        for x_values in x.transpose()[1:]:
            x_val, p = normalization(x_values)
            x_temp.append(x_val)
            norm_p.append(p)
        x = np.array(x_temp).transpose()

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
    return [f_theta, norm_p]
