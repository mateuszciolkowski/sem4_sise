from layer import *

def __init__(self, layer_sizes, activation_function, activation_derivative):
    self.layers = []
    self.activation_function = activation_function #funcke aktywacji
    self.activation_derivative = activation_derivative

    for i in range(1, len(layer_sizes)):
        self.layers.append(Layer(layer_sizes[i], layer_sizes[i - 1], activation_function))

def train(X, y, epochs):

def predict(X):

#TO DO propagacja wstecz i w przod
#W każdej epoce prezentowane są sieci wszystkie wzorce treningowe,
#przy czym program powinien udostępniać możliwość wyboru pomiędzy
# niezmienną oraz losową kolejnością ich prezentacji.


#Program ma także umożliwiać określenie, czy w trakcie nauki ma być
# uwzględniany człon momentum, czy nie.

# W każdej epoce prezentowane są sieci wszystkie wzorce treningowe,
# przy czym program powinien udostępniać możliwość wyboru pomiędzy
# niezmienną oraz losową kolejnością ich prezentacji.