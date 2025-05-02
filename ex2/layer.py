from neuron import *

class Layer:
    def __init__(self, number_of_neurons, number_of_inputs, activation_function, activation_derivative, bias=0.0):
        self.neurons = [
            Neuron(number_of_inputs, activation_function, activation_derivative, bias)
            for _ in range(number_of_neurons)
        ]

    def forward(self, inputs):
        return [neuron.forward(inputs) for neuron in self.neurons]