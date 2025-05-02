from mlp import MLP  # lub bezpośrednio, jeśli masz w tym samym pliku
import numpy as np
from data import load_iris
from utils import *

# Załaduj dane
X, Y = load_iris("data/iris/iris.data", standarded=True)

# Zainicjuj sieć MLP
mlp = MLP(
    layer_sizes=[4, 5, 3],  # 4 wejścia (cechy), 5 neuronów ukrytych, 3 wyjścia (klasy)
    activation_function=sigmoid,
    activation_derivative=sigmoid_derivative
)

# Parametry uczenia (dodaj do klasy MLP lub ustaw ręcznie)
mlp.learning_rate = 0.1
mlp.use_bias = True
mlp.use_momentum = True
mlp.momentum = 0.9

# Trenuj sieć
mlp.train(X, Y, epochs=500, shuffle=True)