import os
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

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

    plt.savefig("filename.png", dpi=300, bbox_inches='tight')

    plt.show()

def clear_log_file(log_filename):
    log_dir = "data/mlp/logs"
    file_path = os.path.join(log_dir, log_filename)
    with open(file_path, 'w') as log_file:
        log_file.truncate(0)  # Usuwa zawartość pliku

