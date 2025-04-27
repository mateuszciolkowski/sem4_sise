from neuron import *

class Layer:
    def __init__(self, number_of_neurons, number_of_inputs, activation_function):
        self.neurons = [Neuron(number_of_inputs, activation_function) for _ in range(number_of_neurons)]

    def forward(self, inputs):
        #Propagacja w przód dla wszystkich neuronów w warstwie.
        return [neuron.forward(inputs) for neuron in self.neurons]
