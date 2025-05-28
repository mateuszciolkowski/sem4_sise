from DataLoader import RiceDataLoader
from Tree import *

def main():
    tree = Tree("data/Rice_Cammeo_Osmancik.arff")
    # wartosc ktora podamy to tyle ile bedziemy miec do testowania reszta to treningowe dane
    # tree.change_tree_parameter(criterion=entropy)
    tree.set_test_size(0.3)
    tree.train()
    tree.predict()
    tree.visualize()

if __name__ == "__main__":
    main()