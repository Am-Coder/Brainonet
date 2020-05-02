import os
import time
import gc
import argparse

# data science imports
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
import pickle

# utils import
from fuzzywuzzy import fuzz


class KnnRecommender:
    """
    This is an item-based collaborative filtering recommender with
    KNN implmented by sklearn
    """
    def __init__(self, path_dataset):
        """
        Recommender requires path to data
        """
        self.path_dataset = path_dataset
        self.model = KNeighborsClassifier()

    def set_model_params(self, n_neighbors=2, algorithm='auto', metric='euclidean', n_jobs=None):
        """
        set model params for sklearn.neighbors.NearestNeighbors

        Parameters
        ----------
        n_neighbors: int, optional (default = 5)

        algorithm: {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional

        metric: string or callable, default 'minkowski', or one of
            ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']

        n_jobs: int or None, optional (default=None)
        """
        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _prep_data(self):
        """
        prepare data for recommender
        """
        # read data
        df_blogs = pd.read_csv(
            self.path_dataset,
            )
        return df_blogs

    def train(self):
        df = self._prep_data()
        y = df['bpk']
        x = df.drop('bpk', axis=1)
        self.model.fit(x, y)
        with open(os.path.join('knn_pickle'), 'wb') as kp:
            pickle.dump(self.model, kp)

    def _inference(self, x_input):
        """
        return top n similar movie recommendations based on user's input movie
        """

        # open pickled model
        loaded_model = pickle.load(open(os.path.join('knn_pickle'), 'rb'))
        result = loaded_model.predict(x_input)

        return result

    def make_recommendations(self, x_input):
        """
        make top n movie recommendations

        Parameters
        ----------
        """
        res = self._inference(x_input)
        print(res)

