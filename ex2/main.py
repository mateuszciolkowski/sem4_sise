import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from data import load_iris, load_auto_association
from mlp import MLP
from utils import *
from interface import *

def main():
    # X, y = load_iris("data/iris/iris.data", standarded=True)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, stratify=y)
    #
    # # Stwórz sieć: 4 wejścia, 1 warstwa ukryta (np. 6 neuronów), 3 wyjścia
    # mlp = MLP(layer_sizes=[4, 5, 3], activation_function=sigmoid, activation_derivative=sigmoid_derivative,learning_rate=0.1,use_momentum=True,momentum=0.9)
    #
    # # Trenuj sieć
    # mlp.train(X_train, y_train, epochs=1000, error_threshold=0.00001, log_interval=10)
    # mlp.save_log_of_learning(10,"network_log.json")
    # plot_error_curve(mlp.epoch_errors)
    # mlp.save_to_file("network.json")
    # mlp_restored = mlp.load_from_file("network.json",sigmoid, sigmoid_derivative)
    #
    # y_true = np.argmax(y_test, axis=1)
    # # outputs = mlp.predict(X_test)
    # outputs = mlp_restored.predict_with_logging(X_test, y_true)
    #
    # # Konwersja predykcji (argmax) i etykiet rzeczywistych
    # y_pred = np.argmax(outputs, axis=1)
    # #
    # # # Ocena
    # print("\nConfusion Matrix:")
    # print(confusion_matrix(y_true, y_pred))
    # #
    # print("\nClassification Report:")
    # print(classification_report(y_true, y_pred, target_names=["setosa", "versicolor", "virginica"]))


    # auto_association_data = np.array([[1, 0, 0, 0],
    #                                   [0, 1, 0, 0],
    #                                   [0, 0, 1, 0],
    #                                   [0, 0, 0, 1]])

    # Tworzymy sieć MLP o odpowiedniej strukturze (autoenkoder)
    # Warstwa wejściowa: 4 neurony, warstwa ukryta: 2 neurony, warstwa wyjściowa: 4 neurony
    # mlp = MLP(layer_sizes=[4, 2, 4],
    #           activation_function=sigmoid,
    #           activation_derivative=sigmoid_derivative,
    #           learning_rate=0.2,
    #           use_momentum=True,momentum=0.6,bias=2.0)
    #
    # # Trening autoenkodera - dane wejściowe i wyjściowe są identyczne
    # mlp.train(auto_association_data, auto_association_data, epochs=10000, error_threshold=0.00001, log_interval=10)
    #
    # # Zapis logów do pliku (opcjonalnie)
    # mlp.save_log_of_learning(10, "autoencoder_log.json")
    #
    # # Wizualizacja wykresu błędów
    # plot_error_curve(mlp.epoch_errors)
    #
    # # Testujemy autoenkoder na tych samych danych wejściowych
    # print("\nAutoencoder learned patterns:")
    # for i, pattern in enumerate(auto_association_data):
    #     output = mlp.predict([pattern])
    #     print(f"Input: {pattern} -> Output: {output[0]}")
    menu = Interface()
    menu.menu()

if __name__ == "__main__":
    main()
