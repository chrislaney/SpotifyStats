from sklearn.cluster import KMeans
from utils import gen_train_matrix

class Clusterer():
    def __init__(self, users):
        train_data, user_ids = gen_train_matrix(users)
        self.algo = KMeans(n_clusters=12, init='random', n_init=20)
        self.algo.fit(train_data)
        labels = self.algo.labels_

    def get_furthest_n_clusters(self, user):

