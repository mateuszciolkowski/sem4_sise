from idlelib import tree

from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier, plot_tree

from DataLoader import *


class Tree:
    def __init__(self, filename):
        self.test_size = None
        self.filename = filename
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.tree = DecisionTreeClassifier()

    """
    fit - określna wage dla każdej cechy, poprzez znajdowanie najlepszego podziału. 
        Dla każdego węzła:
        dla każdej cechy w zbiorze wybieramy możliwą najlepszą wartość progu (cecha <= wartość)
        prawo - próbki niespełniające, lewo - spełniające i obliczamy jak dobrze ten podział rodziela klasy 
    """

    def train(self):
        self.tree.fit(self.X_train, self.y_train)
        train_pred = self.tree.predict(self.X_train)
        train_acc = accuracy_score(self.y_train, train_pred)
        # print(f"Dokładność na zbiorze treningowym: {train_acc:.4f}")

    def predict(self,mode=False):
        y_pred = self.tree.predict(self.X_test)
        test_acc = accuracy_score(self.y_test, y_pred)
        if mode:
            print(f"Dokładność na zbiorze testowym: {test_acc:.4f}")
            print("\nMacierz pomyłek:")
            print(confusion_matrix(self.y_test, y_pred))
            print("\nRaport klasyfikacji:")
            print(classification_report(self.y_test, y_pred, target_names=['Cammeo', 'Osmancik']))

            # Sprawdzenie overfittingu
            train_pred = self.tree.predict(self.X_train)
            train_acc = accuracy_score(self.y_train, train_pred)

            if train_acc - test_acc > 0.1:  # próg 10%
                print("\nUwaga: Możliwe przeuczenie modelu (overfitting).")
            else:
                print("\nModel nie wykazuje wyraźnego przeuczenia.")
            print("\n")
        return y_pred, test_acc

    """
    criterion --> okresla jak oceniamy jakosc podzialu danych w kazdym wezle drzewa 
        opcje:
        *gini -domyślne -- im mniejsza wartosc tym bardziej czysty zbior jeden gatrunek ryzu dominuje w lisciu 
        *enrtopy -- mierzy niepewność/nieuporządkowanie klas, im mniejsza wartość entropi tym bardziej dominuje jedna klasa
                wolniejsze niż gini
        * log_loss -- logarytmicznie obliczany błąd - miara jakości podziału,
                mierzy jak dobrze podział zwiększa prawdopobieństwo poprawnej klasyfikacji 
    class_weight --> pozwala ustawić wagi dla poszczególnych klas, - przydatne przy niezbalansowanych zbierach danych
        *none -- domyślne - wszystnie traktowane tak samo
        *balanced -- przypisuje wagi odwrotnie proporcjonalne do częstości klas, poprawia nauke przy nierównym rozkładzie klas 
        *słownik np {0:1 1:5} - ręczne dobranie 
    splitter --> strategi podziału w węźle decyzyjnym
        *best - domyslny -- wybierane jest najlepszy możliwy podział spośród wszystich cech i progów
        *random -- drzewo wybiera losowo podział spośród najlepszych podziałów 
                - może pomóc w redukcji nadmiernego dopasowania 
                
    max_depth --> maksymalna głębokość drzewa
    * ogranicza maksymalną liczbę poziomów drzewa,
    * mniejsze wartości zapobiegają nadmiernemu dopasowaniu (overfittingowi),
    * domyślnie brak ograniczenia (drzewo rośnie do momentu spełnienia innych kryteriów)

    min_samples_split --> minimalna liczba próbek wymagana do podziału węzła
        * jeśli węzeł ma mniej próbek niż ta wartość, nie jest dzielony,
        * zwiększenie tej wartości powoduje mniej rozgałęzień, czyli prostsze drzewo (mniej overfittingu),
        * domyślnie 2
    
    min_samples_leaf --> minimalna liczba próbek wymagana w liściu drzewa
        * zapewnia minimalną liczbę próbek w końcowym węźle,
        * pomaga uniknąć bardzo małych liści, co zwiększa ogólną uogólnialność modelu,
        * domyślnie 1
    
    ccp_alpha --> parametr do przycinania drzewa (cost complexity pruning)
        * kontroluje złożoność drzewa poprzez koszt złożoności,
        * większa wartość powoduje mocniejsze przycinanie drzewa,
        * pomaga zwalczać overfitting przez usuwanie mało istotnych gałęzi,
        * domyślnie 0 (brak przycinania)
    """

    def change_tree_parameter(self, criterion=None, class_weight=None, splitter=None,
                              max_depth=None, min_samples_split=None, min_samples_leaf=None, ccp_alpha=None):
        self.tree = DecisionTreeClassifier(
            criterion=criterion if criterion is not None else self.tree.criterion,
            class_weight=class_weight if class_weight is not None else self.tree.class_weight,
            splitter=splitter if splitter is not None else self.tree.splitter,
            max_depth=max_depth if max_depth is not None else self.tree.max_depth,
            min_samples_split=min_samples_split if min_samples_split is not None else self.tree.min_samples_split,
            min_samples_leaf=min_samples_leaf if min_samples_leaf is not None else self.tree.min_samples_leaf,
            ccp_alpha=ccp_alpha if ccp_alpha is not None else self.tree.ccp_alpha
        )

    def set_test_size(self, test_size):
        self.test_size = test_size
        self.X_train, self.X_test, self.y_train, self.y_test = RiceDataLoader.load_test_data(self.filename,
                                                                                             self.test_size)

    """
    Kolory oznaczaja klase 
    """

    def visualize(self,filename):
        num_features = self.X_train.shape[1]
        feature_names = ['Area', 'Perimeter', 'Major_Axis_Length', 'Minor_Axis_Length', 'Eccentricity', 'Convex_Area',
                         'Extent']

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
        plt.savefig(filename+".pdf", bbox_inches='tight')
        plt.show()


    def showImportance(self):
        feature_names = ['Area', 'Perimeter', 'Major_Axis_Length', 'Minor_Axis_Length', 'Eccentricity', 'Convex_Area',
                         'Extent']
        feature_importance = self.tree.feature_importances_
        print("Feature importance:")
        for name, importance in zip(feature_names, feature_importance):
            print(f"{name}: {importance:.4f}")
