import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from data import load_iris, load_auto_association
from mlp import MLP
from utils import *
from interface import *

def main():
    menu = Interface()
    menu.menu()

if __name__ == "__main__":
    main()
