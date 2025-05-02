from layer import *
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
import numpy as np

class MLP:
    """
    learning_rate -- wspolczynnik nauki
    use_momentum -- przelacznik czy uzyc momentum
    """
    def __init__(self, layer_sizes, activation_function, activation_derivative,
                 learning_rate=0.1, bias=0.0, use_momentum=False, momentum=0.9):
        self.layers = []
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative
        self.learning_rate = learning_rate
        self.bias = bias
        self.use_momentum = use_momentum
        if self.use_momentum:
            self.momentum = momentum

        #warstwa wejsciowa sa dane nie ma reprezentacji layer
        #tworzenie warstw w ktorych kazda z nich ma okreslona liczbe neuronow
        for i in range(1, len(layer_sizes)):
            self.layers.append(
                #layer_sizes[i] -- ilosc neuronow w warstwie
                #layer_sizes[i-1] -- ilosc neuronow w warstwie poprzedniej
                Layer(layer_sizes[i], layer_sizes[i - 1], activation_function, activation_derivative, bias))

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, expected_outputs):
        # Oblicz delty dla warstwy wyjściowej
        last_layer = self.layers[-1]
        for i, neuron in enumerate(last_layer.neurons):
            error = expected_outputs[i] - neuron.output
            neuron.delta = error * neuron.derivative(neuron.output)

        # Ukryte warstwy (w odwrotnej kolejności)
        for l in reversed(range(len(self.layers) - 1)):
            current_layer = self.layers[l]
            next_layer = self.layers[l + 1]
            for i, neuron in enumerate(current_layer.neurons):
                error = sum(next_neuron.weights[i] * next_neuron.delta for next_neuron in next_layer.neurons)
                neuron.delta = error * neuron.derivative(neuron.output)

    def update_weights(self, inputs):
        #przechodzimy po wszystkich warstwach
        for i, layer in enumerate(self.layers):
            #jesli jest to pierwsza warstwa uzywamy danych wejsciowych
            #dla pozostalych wejsciem sa wyjscia neuronow warstwy poprzedniej
            input_to_use = inputs if i == 0 else [n.output for n in self.layers[i - 1].neurons]
            for neuron in layer.neurons:
                #przechodzimy po ilosci wejsc w neuronie = ilosci wag
                for j in range(len(neuron.weights)):
                    #obliczanie zmiany wagi
                    #wynik propagacji wstecznej
                    delta = self.learning_rate * neuron.delta * input_to_use[j]
                    #jesli uzywamy momentum dodajemy moment "pedu"
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

    # Zostało dodane zatrzymanie poprzez podanie poziomu błędu, nieosiągalność wyniku obliczany za pomocą zmiennej określającej ilość
    # epok bez poprawy błędu, dodane logowanie co interwał epok
    def train(self, X, y, epochs=1000, shuffle=True, error_threshold=None, max_no_improvement_epochs=100, log_interval=10):
        no_improvement_count = 0
        best_error = float('inf')

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

            print(f"Epoch {epoch + 1}, Error: {total_error}")

            if error_threshold and total_error < error_threshold:
                print(f"Error threshold reached. Stopping training.")
                break

            if total_error < best_error:
                best_error = total_error
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if error_threshold is not None and no_improvement_count >= max_no_improvement_epochs:
                print(f"No improvement for {max_no_improvement_epochs} epochs. Stopping training.")
                break

            log_error_to_file(epoch+1,total_error,log_interval=log_interval)

    def predict(self, X):
        return [self.forward(inputs) for inputs in X]

    def evaluate(model, X_test, y_test):

        # Predykcja
        predictions = model.predict(X_test)

        # Zamiana na klasy (najwyższy indeks z wektora wyjściowego)
        y_true = np.argmax(y_test, axis=1)
        y_pred = np.argmax(predictions, axis=1)

        # Accuracy
        acc = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {acc * 100:.2f}%")

        # Macierz pomyłek
        cm = confusion_matrix(y_true, y_pred)
        print("Confusion Matrix:")
        print(cm)

        # Precision, Recall, F1 dla każdej klasy
        precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average=None)
        for i in range(len(precision)):
            print(f"Class {i}: Precision={precision[i]:.2f}, Recall={recall[i]:.2f}, F1={f1_score[i]:.2f}")

        return acc, cm, precision, recall, f1_score


def log_error_to_file(epoch, error, log_filename="error_log.txt", log_interval=10):
    if epoch % log_interval == 0:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{epoch}, {error}\n")


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

