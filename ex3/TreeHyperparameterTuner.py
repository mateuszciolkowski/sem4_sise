from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import Tree

class TreeHyperparameterTuner:
    def __init__(self, filename, test_size=0.3):
        self.filename = filename
        self.test_size = test_size
        self.param_dist = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': range(2, 20),
            'min_samples_leaf': range(1, 10),
            'ccp_alpha': [0.0, 0.01, 0.05, 0.1],
            'criterion': ['gini', 'entropy', 'log_loss']
        }

    def _train_and_score(self, **params):
        tree_obj = Tree.Tree(self.filename)
        tree_obj.set_test_size(self.test_size)
        tree_obj.change_tree_parameter(**params)
        tree_obj.train()
        _, accuracy = tree_obj.predict()
        return accuracy

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

        best_score = -np.inf
        best_params = None

        for i, params in enumerate(param_list):
            print(f"\n Testowanie parametrów {i+1}/{n_iter}: {params}")
            score = self._train_and_score(**params)
            print(f" Dokładność: {score:.4f}")
            results.append((score, params))
            if score > best_score:
                best_score = score
                best_params = params

        print("\ Najlepsze parametry:", best_params)
        print(f" Najlepsza dokładność: {best_score:.4f}")

        return best_params, best_score
