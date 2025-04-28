import numpy as np
from sklearn.preprocessing import StandardScaler

def load_iris(fileName, standarded = False):
    iris_features = []
    iris_labels = []
    with open(fileName, 'r') as file:
        for line in file:
            line_data = line.strip().split(',')
            raw_features = list(map(float,line_data[:4]))
            label = line_data[4]
            iris_features.append(raw_features)
            iris_labels.append(label)

    #utworzenie numpy array do zbioru danych cech oraz rozwiazan
    X = np.array(iris_features)
    Y = np.array(iris_labels)

    # if standarded:
    #     scaler = StandardScaler()
    #     X = scaler.fit_transform(X)
    #     Y = scaler.transform(Y)

    return X, Y
