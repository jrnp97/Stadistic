import matplotlib.pyplot as plt
# from  import run as process
from taller import run as process

if __name__ == "__main__":
    n = 5
    # -- Run training and process evaluation n times -- #
    errors = []
    i = 1
    while i <= n:
        print("Init process #{0}".format(i))
        e = process(norm=False, alpha=0.0000001)
        print("Finish process #{0}".format(i))
        errors.append(e)
        i += 1
    plt.plot(errors)
    plt.show()
