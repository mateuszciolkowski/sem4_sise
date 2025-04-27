from layer import *

def __init__(self, layer_sizes, activation_function, activation_derivative):
    self.layers = []
    self.activation_function = activation_function #funcke aktywacji
    self.activation_derivative = activation_derivative

    for i in range(1, len(layer_sizes)):
        self.layers.append(Layer(layer_sizes[i], layer_sizes[i - 1], activation_function))


#TO DO propagacja wstecz i w przod