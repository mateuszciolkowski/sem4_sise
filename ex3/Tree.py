from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier, plot_tree

from DataLoader import *

class Tree:
    def __init__(self,filename):
        self.test_size = None
        self.filename = filename
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.tree = DecisionTreeClassifier()

    def train(self):
        self.tree.fit(self.X_train, self.y_train)

    def predict(self):
        y_pred = self.tree.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"dokladnosc: {accuracy:.4f}")

        print("\nMacierz pomyłek:")
        print(confusion_matrix(self.y_test, y_pred))

        print("\nRaport klasyfikacji:")
        print(classification_report(self.y_test, y_pred, target_names=['Cammeo', 'Osmancik']))

        return y_pred, accuracy


    """
    criterion --> okresla jak oceniamy jakosc podzialu danych w kazdym wezle drzewa 
        opcje:
        *gini -- im mniejsza wartosc tym bardziej czysty zbior jeden gatrunek ryzu dominuje w lisciu 
        *enrtopy -- 
    class_weight --> 
    splitter --> 
    """
    def change_tree_parameter(self, criterion=None, class_weight=None, splitter=None):
        self.tree = DecisionTreeClassifier(
            criterion=criterion if criterion is not None else self.tree.criterion,
            class_weight=class_weight if class_weight is not None else self.tree.class_weight,
            splitter=splitter if splitter is not None else self.tree.splitter
        )

    def set_test_size(self,test_size):
        self.test_size = test_size
        self.X_train, self.X_test, self.y_train, self.y_test = RiceDataLoader.load_test_data(self.filename, self.test_size)

    """
    Kolory oznaczaja klase 
    """
    def visualize(self):
        num_features = self.X_train.shape[1]
        feature_names = [f'feat{i}' for i in range(num_features)]

        plt.figure(figsize=(95, 30))  # szerokość bardzo duża, wysokość jak wcześniej
        plot_tree(
            self.tree,
            filled=True,
            feature_names=feature_names,
            class_names=['Cammeo', 'Osmancik'],
            fontsize=8,
            rounded=True,
            proportion=True,
            precision=2,
            label='all'
        )
        plt.tight_layout(pad=3.0)
        plt.savefig("tree.pdf", bbox_inches='tight')
        plt.show()




