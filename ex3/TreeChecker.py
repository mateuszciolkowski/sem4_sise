from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import Tree

class TreeChecker:
    def __init__(self, filename, test_size=0.3):
        self.filename = filename
        self.test_size = test_size
        self.param_dist = {
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 3, 4],
            'min_samples_leaf': [1, 2],
            'ccp_alpha': [0.0, 0.001, 0.005],
            'class_weight': [None, 'balanced'],
            'criterion': ['gini', 'entropy', 'log_loss'],
            'splitter': ['random', 'best']
        }

    def _train_and_score(self, **params):
        tree_obj = Tree.Tree(self.filename)
        tree_obj.set_test_size(self.test_size)
        tree_obj.change_tree_parameter(**params)
        tree_obj.train()
        _, accuracy = tree_obj.predict()
        return accuracy,tree_obj

    def tune(self, param_dist, n_iter=50, cv=3, random_state=42):
        results = []
        rng = np.random.default_rng(random_state)
        param_list = []
        keys = list(param_dist.keys())

        for _ in range(n_iter):
            params = {}
            for k in keys:
                v = param_dist[k]
                params[k] = rng.choice(list(v)) if isinstance(v, (list, range)) else v
            param_list.append(params)

        best_tree = None
        worst_tree = None
        best_score = -np.inf
        worst_score = np.inf
        best_params = None
        worst_params = None

        for i, params in enumerate(param_list):
            score,tree_obj = self._train_and_score(**params)
            results.append((score, params))
            if score > best_score:
                best_tree = tree_obj
                best_score = score
                best_params = params
            if score < worst_score:
                worst_tree = tree_obj
                worst_score = score
                worst_params = params

        best_tree.visualize("best")
        best_tree.showImportance()
        print(f"Najlepsze parametry:{best_params}")
        print(f"Najlepsza dokładność: {best_score:.4f}")
        best_tree.predict(True)

        worst_tree.visualize("worst")
        worst_tree.showImportance()
        print(f"Najgorsze parametry:{worst_params}")
        print(f"Najgorsza dokładność: {worst_score:.4f}")
        worst_tree.predict(True)



