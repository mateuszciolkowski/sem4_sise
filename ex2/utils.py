import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(f):
    return f * (1 - f)