# from mlp import MLP  # lub bezpośrednio, jeśli masz w tym samym pliku
# from data import load_iris, load_auto_association
# from utils import *
#
# X, Y = load_iris("data/iris/iris.data", standarded=True)
# # X, Y = load_auto_association()
#
# mlp = MLP(
#     layer_sizes=[4, 5, 3],  # 4 wejścia (cechy), 5 neuronów ukrytych, 3 wyjścia (klasy)
#     activation_function=sigmoid,
#     activation_derivative=sigmoid_derivative
# )
#
# # Parametry uczenia
# mlp.learning_rate = 0.1
# mlp.use_bias = True
# mlp.use_momentum = True
# mlp.momentum = 0.9
#
# # Trenuj sieć
# mlp.train(X, Y, epochs=10000, shuffle=True)

import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from data import load_iris, load_auto_association
from mlp import MLP
from utils import sigmoid, sigmoid_derivative


def main():
    X, y = load_iris("data/iris/iris.data", standarded=True)

    # Podział danych (80% trening, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Stwórz sieć: 4 wejścia, 1 warstwa ukryta (np. 6 neuronów), 3 wyjścia
    mlp = MLP(layer_sizes=[4, 6, 3], activation_function=sigmoid, activation_derivative=sigmoid_derivative)

    # Trenuj sieć
    mlp.train(X_train, y_train, epochs=2000, error_threshold=0.01, log_interval=10)

    # Predykcja na zbiorze testowym
    outputs = mlp.predict(X_test)

    # Konwersja predykcji (argmax) i etykiet rzeczywistych
    y_pred = np.argmax(outputs, axis=1)
    y_true = np.argmax(y_test, axis=1)

    # Ocena
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["setosa", "versicolor", "virginica"]))

if __name__ == "__main__":
    main()
