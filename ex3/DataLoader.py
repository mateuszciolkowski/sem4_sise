import arff
import numpy as np
from pyexpat import features

from sklearn.model_selection import train_test_split


class RiceDataLoader:

    @staticmethod
    def load_data(filepath):
        with open(filepath, 'r') as f:
            dataset = arff.load(f)

        data = list(dataset['data'])
        attributes = dataset['attributes']

        class_attr = attributes[-1]
        class_attr_name = class_attr[0]
        class_names = class_attr[1]

        class_mapping = {cls_name.decode('utf-8') if isinstance(cls_name, bytes) else cls_name: i
                         for i, cls_name in enumerate(class_names)}

        X, y = [], []

        for row in data:
            features_row = list(row)[:-1]
            label = row[-1]
            if isinstance(label, bytes):
                label = label.decode('utf-8')
            X.append(features_row)
            y.append(class_mapping[label])

        features = np.array(X, dtype=np.float32)
        labels = np.array(y, dtype=np.int32)

        return features, labels

    @staticmethod
    def load_test_data(filename,test_size):
        features,labels = RiceDataLoader.load_data(filename)
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=test_size, random_state=None, shuffle=True)
        return X_train, X_test, y_train, y_test
