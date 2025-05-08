from neuron import *

class Layer:
    def __init__(self, number_of_neurons, number_of_inputs, activation_function, activation_derivative, bias=0.0, is_processing=True):
        self.neurons = [
            Neuron(number_of_inputs, activation_function, activation_derivative, bias, is_processing)
            for _ in range(number_of_neurons)
        ]

    def forward(self, inputs):
        return [neuron.forward(inputs) for neuron in self.neurons]