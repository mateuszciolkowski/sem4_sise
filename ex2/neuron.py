import random
import math

class Neuron:
    def __init__(self, number_of_inputs, activation_function):
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(number_of_inputs)]  # Losowe wagi
        self.bias = random.uniform(-0.5, 0.5)  # Losowe obciążenie
        self.activation_function = activation_function  # Funkcja aktywacji
        self.output = None  # Wyjście neuronu

    def forward(self, inputs):
        #Propagacja w przód - oblicza wyjście neuronu na podstawie wejść.
        weighted_sum = sum(i * w for i, w in zip(inputs, self.weights)) + self.bias
        self.output = self.activation_function(weighted_sum)
        return self.output

    def derivative(self, output):
        #Pochodna funkcji aktywacji (używana w propagacji wstecznej)
        #Dla funkcji sigmoidalnej: f'(x) = f(x) * (1 - f(x))
        return output * (1 - output)