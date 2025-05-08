import random
import numpy as np
import json
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from datetime import datetime
from layer import Layer

class MLP:
    def __init__(self, layer_sizes, activation_function, activation_derivative,
                 learning_rate=0.1, bias=0.0, use_momentum=False, momentum=0.9):
        self.epoch_errors = None
        self.layers = []
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative
        self.learning_rate = learning_rate
        self.bias = bias
        self.use_momentum = use_momentum
        self.momentum = momentum if use_momentum else 0.0

        for i in range(1, len(layer_sizes)):
            self.layers.append(
                Layer(layer_sizes[i], layer_sizes[i - 1], activation_function, activation_derivative, bias)
            )

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, expected_outputs):
        last_layer = self.layers[-1]
        for i, neuron in enumerate(last_layer.neurons):
            error = expected_outputs[i] - neuron.output
            neuron.delta = error * neuron.derivative(neuron.output)

        for l in reversed(range(len(self.layers) - 1)):
            current_layer = self.layers[l]
            next_layer = self.layers[l + 1]
            for i, neuron in enumerate(current_layer.neurons):
                error = sum(next_neuron.weights[i] * next_neuron.delta for next_neuron in next_layer.neurons)
                neuron.delta = error * neuron.derivative(neuron.output)

    def update_weights(self, inputs):
        for i, layer in enumerate(self.layers):
            input_to_use = inputs if i == 0 else [n.output for n in self.layers[i - 1].neurons]
            for neuron in layer.neurons:
                for j in range(len(neuron.weights)):
                    delta = self.learning_rate * neuron.delta * input_to_use[j]
                    if self.use_momentum:
                        delta += self.momentum * neuron.last_weight_changes[j]
                        neuron.last_weight_changes[j] = delta
                    neuron.weights[j] += delta
                if self.bias:
                    delta_b = self.learning_rate * neuron.delta
                    if self.use_momentum:
                        delta_b += self.momentum * neuron.last_bias_change
                        neuron.last_bias_change = delta_b
                    neuron.bias += delta_b

    def train(self, X, y, epochs=1000, shuffle=True, error_threshold=None,
              max_no_improvement_epochs=100, log_interval=10):
        no_improvement_count = 0
        best_error = float('inf')
        self.epoch_errors = []  # Przechowuje błędy globalnie w instancji

        for epoch in range(epochs):
            samples = list(zip(X, y))
            if shuffle:
                random.shuffle(samples)

            total_error = 0
            for inputs, target in samples:
                outputs = self.forward(inputs)
                self.backward(target)
                self.update_weights(inputs)
                total_error += sum((t - o) ** 2 for t, o in zip(target, outputs))

            self.epoch_errors.append(total_error)

            if (epoch + 1) % log_interval == 0:
                print(f"Epoch {epoch + 1}, Error: {total_error}")

            if error_threshold and total_error < error_threshold:
                print(f"Error threshold reached at epoch {epoch + 1}. Stopping training.")
                break

            if total_error < best_error:
                best_error = total_error
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if error_threshold is not None and no_improvement_count >= max_no_improvement_epochs:
                print(f"No improvement for {max_no_improvement_epochs} epochs. Stopping training.")
                break


    def save_log_of_learning(self, interval, filename="log_filename.json"):
        filename = f"data/mlp/{filename}"
        log_data = []

        for epoch, error in enumerate(self.epoch_errors):
            if epoch % int(interval) == 0:
                log_data.append({"epoch": epoch, "error": error})

        with open(filename, 'w') as log_file:
            json.dump(log_data, log_file, indent=4)


    def predict(self, X):
        return [self.forward(inputs) for inputs in X]

    def evaluate(self, X_test, y_test):
        predictions = self.predict(X_test)
        y_true = np.argmax(y_test, axis=1)
        y_pred = np.argmax(predictions, axis=1)

        acc = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {acc * 100:.2f}%")

        cm = confusion_matrix(y_true, y_pred)
        print("Confusion Matrix:")
        print(cm)

        precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average=None)
        for i in range(len(precision)):
            print(f"Class {i}: Precision={precision[i]:.2f}, Recall={recall[i]:.2f}, F1={f1_score[i]:.2f}")

        return acc, cm, precision, recall, f1_score

    def save_to_file(self, filename=None):
        if filename is None:
            filename = "network_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
        filename = f"data/mlp/{filename}"

        model_data = {
            "learning_rate": self.learning_rate,
            "bias": self.bias,
            "use_momentum": self.use_momentum,
            "momentum": self.momentum,
            "layer_sizes": [len(self.layers[0].neurons[0].weights)] + [len(layer.neurons) for layer in self.layers],
            "layers": []
        }

        for layer in self.layers:
            layer_data = []
            for neuron in layer.neurons:
                neuron_data = {
                    "weights": neuron.weights,
                    "bias": neuron.bias
                }
                layer_data.append(neuron_data)
            model_data["layers"].append(layer_data)

        with open(filename, "w") as f:
            json.dump(model_data, f, indent=2)

    @staticmethod
    def load_from_file(filename, activation_function, activation_derivative):
        filename = f"data/mlp/{filename}"
        with open(filename, "r") as f:
            data = json.load(f)

        mlp = MLP(
            layer_sizes=data["layer_sizes"],
            activation_function=activation_function,
            activation_derivative=activation_derivative,
            learning_rate=data["learning_rate"],
            bias=data["bias"],
            use_momentum=data["use_momentum"],
            momentum=data.get("momentum", 0.0)
        )

        for layer_data, layer in zip(data["layers"], mlp.layers):
            for neuron_data, neuron in zip(layer_data, layer.neurons):
                neuron.weights = neuron_data["weights"]
                neuron.bias = neuron_data["bias"]

        return mlp


#TO DO zapis sieci do pliku
# zapis wag ktore zostaly nauczone ? - NIE KUMAM TROCHE O CO CHODZI Z ZAPISEM WAG
# do zrobienia tryb testowania predcit propagacja w przod - TEGO NIE MA?
# podzielic dane jakies irysow by moc testowac - ZROBIONY TRAINER JAKO KLASA DO WYWOŁYWANIA W MAINIE
# moze zobaczyc jak dzialalo to na KAD przy knn

# RACZEJ DZIAŁA - TAK MI SIE WYDAJE
#ZOBACZYC CZY TAK TO U NAS DZIALA
# Sekwencja czynności, która zostaje wykonana dla pojedynczego wzorca,
# wygląda tu następująco: wzorzec treningowy podawany jest na wejścia sieci,
# następnie odbywa się jego propagacja w przód, dalej na podstawie wartości
# odpowiedzi wygenerowanej przez sieć oraz wartości pożądanego wzorca odpowiedzi
# następuje wyznaczenie błędów, po czym propagowane są one wstecz, na koniec zaś
# ma miejsce wprowadzenie poprawek na wagi.


#DONE
#Czas trwania nauki powinien być determinowany albo zrealizowaniem wprowadzonej przez użytkownika liczby epok,
#albo osiągnięciem przez sieć podanego przez użytkownika poziomu błędu (należy jednak umożliwić tu zatrzymanie
# nauki w pewnym momencie, gdyby założony poziom błędu okazał się nieosiągalny), albo spełnieniem któregokolwiek
# warunku z dwóch wymienionych.

# BRAK ZATRZYMANIA W DOWOLNYM MOMENCIE, ZATRZYMANIE POPRZEZ BRAK POPRAWY WYNIKU total_error - jeśli był podany błąd
#EPOKI SA trzeba dodac zatrzeymaneie przez blad lub zatrzymanie w dowolnym momencie np

#TO CHECK co zrobione
#TO DO CHYBA

#1
#WCZYTYWANIE I ODZCYTYWANIE Z PLIKOW SIECI
#2
#WCZYTYWANIE ZESTAWOW WZORCOW?
#3
#Logowanie mocniejsze do pliku
# rejestrowanie do pliku pewnych wielkości,
# a mianowicie: wzorca wejściowego, popełnionego
# przez sieć błędu dla całego wzorca,
# pożądanego wzorca odpowiedzi,
# błędów popełnionych na poszczególnych wyjściach sieci,
# wartości wyjściowych neuronów wyjściowych,
# wag neuronów wyjściowych,
# wartości wyjściowych neuronów ukrytych,
# wag neuronów ukrytych (w kolejności warstw od dalszych względem wejść sieci do bliższych).
# Ewentualnie program może umożliwiać użytkownikowi wybór tylko niektórych spośród nich do rejestracji w danym przebiegu.