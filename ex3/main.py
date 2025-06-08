from DataLoader import RiceDataLoader
from Tree import *
from ex3.TreeHyperparameterTuner import TreeHyperparameterTuner


def main():
    tree = Tree("data/Rice_Cammeo_Osmancik.arff")
    # wartosc ktora podamy to tyle ile bedziemy miec do testowania reszta to treningowe dane
    tree.change_tree_parameter(criterion="log_loss", max_depth=10, min_samples_leaf=13, ccp_alpha=0.01)
    tree.set_test_size(0.3)
    tree.train()
    tree.predict()
    tree.showImportance()

    tree.visualize()

    # tuner = TreeHyperparameterTuner("data/Rice_Cammeo_Osmancik.arff", test_size=0.3)
    # best_params, best_score = tuner.tune(tuner.param_dist, n_iter=50)


if __name__ == "__main__":
    main()