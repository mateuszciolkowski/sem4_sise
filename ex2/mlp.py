import random
import numpy as np
import json
from datetime import datetime
from layer import Layer
import os

class MLP:
    def __init__(self, layer_sizes, activation_function, activation_derivative, bias=0.0):
        self.layer_sizes = layer_sizes  # Dodanie atrybutu layer_sizes
        self.layers = []
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative
        self.bias = bias

        # self.epoch_errors = None

        # Kolejne warstwy (ukryte i wyjściowe) - z neuronami, które przetwarzają dane
        for i in range(1, len(layer_sizes)):
            self.layers.append(
                Layer(
                    number_of_neurons=layer_sizes[i],  # Liczba neuronów danej warstwy
                    number_of_inputs=layer_sizes[i - 1],  # Liczba wejść z poprzedniej warstwy
                    activation_function=activation_function,
                    activation_derivative=activation_derivative,
                    bias=bias,
                    is_processing=True  # Przetwarza dane
                )
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

    def update_weights(self, inputs, momentum, learning_rate, use_momentum=False):
        for i, layer in enumerate(self.layers):
            input_to_use = inputs if i == 0 else [n.output for n in self.layers[i - 1].neurons]
            for neuron in layer.neurons:
                for j in range(len(neuron.weights)):
                    delta = learning_rate * neuron.delta * input_to_use[j]
                    if use_momentum:
                        delta += momentum * neuron.last_weight_changes[j]
                        neuron.last_weight_changes[j] = delta
                    neuron.weights[j] += delta
                if self.bias:
                    delta_b = learning_rate * neuron.delta
                    if use_momentum:
                        delta_b += momentum * neuron.last_bias_change
                        neuron.last_bias_change = delta_b
                    neuron.bias += delta_b

    def train(self, X, y, epochs=1000, shuffle=True, error_threshold=None, use_momentum=False, momentum=0.9,
              max_no_improvement_epochs=100, log_interval=10, learning_rate=0.1):
        no_improvement_count = 0
        best_error = float('inf')
        epoch_errors = []  # Przechowuje błędy globalnie w instancji

        for epoch in range(epochs):
            samples = list(zip(X, y))
            if shuffle:
                random.shuffle(samples)

            total_error = 0
            for inputs, target in samples:

                outputs = self.forward(inputs)
                self.backward(target)
                self.update_weights(inputs,learning_rate=learning_rate,momentum=momentum, use_momentum=use_momentum)
                total_error += sum((t - o) ** 2 for t, o in zip(target, outputs))

            epoch_errors.append(total_error)

            if (epoch + 1) % log_interval == 0:
                print(f"Epoch {epoch + 1}, Error: {total_error}")

            if error_threshold and total_error < error_threshold:
                print(f"Error threshold reached at epoch {epoch + 1}. Stopping training.")
                return epoch_errors
                # break



            if total_error < best_error:
                best_error = total_error
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if error_threshold is not None and no_improvement_count >= max_no_improvement_epochs:
                print(f"No improvement for {max_no_improvement_epochs} epochs. Stopping training.")
                return epoch_errors
                # break
        return epoch_errors

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

    def save_to_file(self, filename=None):
        if filename is None:
            filename = "network_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
        filename = f"data/mlp/saved_network/{filename}"

        model_data = {
            "bias": self.bias,
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
        filename = f"data/mlp/saved_network/{filename}"
        with open(filename, "r") as f:
            data = json.load(f)

        mlp = MLP(
            layer_sizes=data["layer_sizes"],
            activation_function=activation_function,
            activation_derivative=activation_derivative,
            bias=data["bias"],
        )

        for layer_data, layer in zip(data["layers"], mlp.layers):
            for neuron_data, neuron in zip(layer_data, layer.neurons):
                neuron.weights = neuron_data["weights"]
                neuron.bias = neuron_data["bias"]

        return mlp

    def predict_with_logging(self, X, y_true=None, log_filename="predict_log.json",
                             weights_filename="weights_log.json",
                             log_inputs=True, log_output_values=True,
                             log_desired_output=True, log_output_errors=True,
                             log_hidden_values=True):
        outputs = []
        log_dir = "data/mlp/logs"
        os.makedirs(log_dir, exist_ok=True)

        # Struktura danych do zapisania w pliku JSON
        log_data = []

        for i, inputs in enumerate(X):
            sample_log = {"sample": i + 1}
            output = self.forward(inputs)
            outputs.append(output)

            if log_inputs:
                sample_log["inputs"] = inputs.tolist() if isinstance(inputs, np.ndarray) else inputs

            # Logowanie wartości wyjściowych (predykcji)
            if log_output_values:
                sample_log["predicted_output"] = output.tolist() if isinstance(output, np.ndarray) else output

            # Logowanie oczekiwanych wyników i błędów
            if y_true is not None:
                expected_class = y_true[i]
                expected = [1 if j == expected_class else 0 for j in range(len(output))]
                error_vector = [t - o for t, o in zip(expected, output)]
                if log_desired_output:
                    sample_log["expected_output"] = expected
                if log_output_errors:
                    sample_log["output_errors"] = error_vector
                    total_error = sum(e ** 2 for e in error_vector)
                    sample_log["total_error"] = total_error

            # Logowanie wartości ukrytych neuronów
            if log_hidden_values:
                hidden_outputs = [
                    [neuron.output for neuron in layer.neurons]
                    for layer in self.layers[:-1]
                ]
                sample_log["hidden_layer_outputs"] = hidden_outputs

            log_data.append(sample_log)

        with open(f"{log_dir}/{log_filename}", "w") as log_file:
            json.dump(log_data, log_file, indent=4)

        weights_data = []

        for layer_idx, layer in enumerate(self.layers):
            layer_data = {"layer": layer_idx + 1, "neurons": []}
            for neuron_idx, neuron in enumerate(layer.neurons):
                neuron_data = {
                    "neuron": neuron_idx + 1,
                    "weights": neuron.weights,
                    "bias": neuron.bias
                }
                layer_data["neurons"].append(neuron_data)
            weights_data.append(layer_data)

        with open(f"{log_dir}/{weights_filename}", "w") as weight_file:
            json.dump(weights_data, weight_file, indent=4)

        print(f"Logowanie zakończone. Dane zapisano do folderu {log_dir}")
        return outputs



