from sklearn.cluster import KMeans
from utils import gen_train_matrix, get_ordered_user_row
'''
Contains Clusterer class, which abstracts clustering away form the KMeans cluster that we use
'''
class Clusterer():
    def __init__(self, users):
        train_data, user_ids = gen_train_matrix(users)
        self.algo = KMeans(n_clusters=12, init='random', n_init=20, random_state=4825) # random_state to limit needing to update users in database
        self.algo.fit(train_data)
        self.labels = self.algo.labels_


    def get_similar_clusters(self, user, n):
        ''' gets n most and n least similar clusters'''
        ordered_genre_row = get_ordered_user_row(user)
        # get distances from each cluster centroid
        distances = self.algo.transform(ordered_genre_row.reshape(1, -1))[0]
        distance_dict = {}

        for cluster, distance in enumerate(distances):
            distance_dict[float(distance)] = int(cluster)
        #keys are distances, so first elements will be closer than second
        distance_tups = sorted(distance_dict.items())
        #get first and last n entries in sorted list
        close_clusters = distance_tups[:n]
        far_clusters = distance_tups[-n:]
        return close_clusters, far_clusters

    def predict(self, user):
        '''returns the int corresponding to a user's cluster; takes in user as a dictionary'''
        ordered_genre_row = get_ordered_user_row(user)
        return int(self.algo.predict(ordered_genre_row.reshape(1, -1))[0])