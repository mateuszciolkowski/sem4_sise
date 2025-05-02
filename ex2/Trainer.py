#przyjmowane [mlp-cala siec], [dane do trenowania], [learning-rate], [ilos epok]
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from mlp import *


class Trainer:
    def __init__(self, model, X, Y, test_size=0.2, random_state=42):
        self.model = model  # Sieć neuronowa
        self.X = X  # Cechy
        self.Y = Y  # Etykiety
        self.test_size = test_size  # Proporcja testowa
        self.random_state = random_state  # Ziarno do losowania (do podziału danych)

    def split_data(self):
        """
        Podział danych na zbiór treningowy i testowy.
        """
        return train_test_split(self.X, self.Y, test_size=self.test_size, random_state=self.random_state)

    def train(self, X_train, Y_train, epochs=1000, shuffle=True, log_interval=10):
        """
        Trening sieci neuronowej.
        """
        self.model.train(X_train, Y_train, epochs=epochs, shuffle=shuffle, log_interval=log_interval)

    def evaluate(self, X_test, Y_test):
        """
        Ocena skuteczności modelu na zbiorze testowym.
        """
        predictions = self.model.predict(X_test)

        # Zmieniamy format Y_test i predictions na klasyczne etykiety (np. indeksy)
        y_true = np.argmax(Y_test, axis=1)
        y_pred = np.argmax(predictions, axis=1)

        # Liczba poprawnie sklasyfikowanych przypadków
        correct_predictions = np.sum(y_true == y_pred)
        print(f"Correctly classified: {correct_predictions}/{len(Y_test)}")

        # Macierz pomyłek
        cm = confusion_matrix(y_true, y_pred)
        print("Confusion Matrix:")
        print(cm)

        # Precision, Recall i F-Measure
        precision, recall, fscore, _ = precision_recall_fscore_support(y_true, y_pred, average=None)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F-Measure:", fscore)

        return cm, precision, recall, fscore


def load_iris_data():
    iris = load_iris()
    X = iris.data  # cechy
    Y = iris.target  # etykiety (0, 1, 2 dla 3 klas)

    # Konwertujemy etykiety na format one-hot
    Y_one_hot = np.zeros((Y.size, 3))
    Y_one_hot[np.arange(Y.size), Y] = 1

    return X, Y_one_hot


