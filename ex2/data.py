import numpy as np
from sklearn.preprocessing import StandardScaler

def load_iris(fileName, standarded = False):
    iris_features = []
    iris_labels = []
    #zmiana nazwy gatunku na format one-hot
    class_map = {
        'Iris-setosa': [1,0,0],
        'Iris-versicolor': [0,1,0],
        'Iris-virginica': [0,0,1],
    }
    with open(fileName, 'r') as file:
        for line in file:
            line_data = line.strip().split(',')
            raw_features = list(map(float,line_data[:4]))
            label = class_map[line_data[4]]
            iris_features.append(raw_features)
            iris_labels.append(label)

    #utworzenie numpy array do zbioru danych cech oraz rozwiazan
    X = np.array(iris_features)
    Y = np.array(iris_labels)

    #standardyzacja danych X
    # (wartosc cechy - srednia cechy)/odchylenie standardowe cechy
    if standarded:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    return X, Y
