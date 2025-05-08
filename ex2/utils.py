import math
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(f):
    return f * (1 - f)

def plot_error_curve(epoch_errors):
    if epoch_errors is None:
        print("Brak danych o błędach do wyświetlenia.")
        return

    plt.plot(epoch_errors)
    plt.title("Krzywa błędu podczas uczenia")
    plt.xlabel("Epoka")
    plt.ylabel("Błąd całkowity")
    plt.grid(True)
    plt.show()
