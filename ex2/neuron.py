import random

"""
number_of_inputs -- ilosc wejsc dla pojedynczego neuronu, np liczba cech 
activation_funcion -- funkcja aktywacji ktora neuron wykorzystuje do obliczenia swojego wyjscia, np: funkcja sigmoidalna 
                        przeksztalca suma wazna wejsc w wyniki ktory neuron wyprodukuje
activation_derivative -- pochodna funckji aktywacji , uzywana w procesie propagacji wstecznej do obliczenia bledu i dostosowania wag
use_bias -- przelacznik w ktorym wybieramy czy uzyjemy bias (przesuniecia do funkcji aktywacji)
"""

class Neuron:
    def __init__(self, number_of_inputs, activation_function, activation_derivative, bias=0.0):
        #wagi sa losowe z zakresu -1,1
        self.weights = [random.randint(-1, 1) for _ in range(number_of_inputs)]
        self.bias = bias
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative

        #output - zmienna ktora bedzie zawierac wynik oblcizen neuronu warosc wyjsciowa po zastosowaniu funkcji aktywacji
        #delta - przechowuje bład neuronu w trakcje propagacji wstecznej , jest obliczana podczas procesu uczenia i pozwla na aktualizacje wag
        self.output = 0.0
        self.delta = 0.0

        #lista zmiana kazdej z cech jeden wpis na kazde wejscie neuronu
        self.last_weight_changes = [0.0 for _ in range(number_of_inputs)]
        #poprzednia zmiana biasu
        self.last_bias_change = 0.0


    #obliczanie wyjscia neuronu na podstawie wejsc i wag
    #wynik po zsumowaniu jest przeksztalcany przez funkcje aktywacji(uzywajac funkcji sigmoidalnej jest to w zakresie 0-1)
    #bez funkcji aktywacji siec bylaby liniowa
    def forward(self, inputs):
        total = 0
        for index in range(len(inputs)):
            total += inputs[index] * self.weights[index]
        total += self.bias
        self.output = self.activation_function(total)
        return self.output

    def derivative(self, output):
        return self.activation_derivative(output)