from layer import *

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

    def train(self, X, y, epochs=1000, shuffle=True):
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

    def predict(self, X):
        return [self.forward(inputs) for inputs in X]


