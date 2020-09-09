import numpy as np
import pandas as pd
from scipy.spatial import distance
from sklearn.model_selection import train_test_split
from surprise import KNNWithMeans, KNNBasic, Dataset, Reader
from src.data_ingestion import BXReader
from src.preprocessing import ratings


# helpers
def scale_df(df, range=(1,10)):
    avg = np.mean(np.arange(start=range[0],stop=range[1]+1))
    return df.apply(lambda x: x-avg)


def cosine_sim(u, v):
    return 1 - distance.cosine(u, v)


class Recommender:

    def __init__(self, ratings_df=ratings):
        self.ratings_df = ratings_df
        self.train_df = None
        self.model = None

    def fit(self, test_frac):
        user_train, user_test = train_test_split(
            self.ratings_df['User'].unique(), test_size=test_frac)

        train_df = self.ratings_df[
            self.ratings_df['User'].isin(user_train)]

        self.train_df = train_df

        # # To use user-based cosine similarity
        sim_options = {
            "name": "cosine",
            "user_based": True,  # Compute similarities between users
        }

        algo = KNNBasic(sim_options=sim_options, k=10)

        # # training our algo

        reader = Reader(rating_scale=(1, 10))
        data = Dataset.load_from_df(train_df[["User", "Book-Title", "Rating"]], reader)

        training = data.build_full_trainset()

        algo.fit(training)

        #  this is the model object with all the functionality needed
        self.model = algo

    def predict(self, new_data):
        books = list(new_data.keys())
        user_item = pd.pivot_table(
            self.train_df.loc[self.train_df['Book-Title'].isin(books)],
            index='User', columns='Book-Title', values='Rating')

        # scaling and fillna on order to be able to compute similarity
        merged = user_item.append(pd.Series(new_data, name="new"))
        merged = scale_df(merged)
        merged = merged.fillna(0)

        #     compute cosine similarity to find closest user from training to
        # test user
        vf = np.vectorize(lambda user: cosine_sim(merged.loc[user], merged.loc['new']))
        sims = pd.Series(vf(merged.index.values[:-1]), index=user_item.index)
        closest = sims.index[sims.argmax()]

        # preds for each book for new user
        get_prediction = lambda b: self.model.predict(uid=closest, iid=b).est
        preds = pd.Series(self.train_df['Book-Title'].unique()).apply(get_prediction)

        keys = self.train_df['Book-Title'].unique()
        return dict(zip(keys, preds))

    def recommend(self, new_data, n=15, return_scores=False):
        d_preds = self.predict(new_data)
        df_largest = pd.DataFrame({
            'title': list(d_preds.keys()),
            'score': list(d_preds.values())}).nlargest(n, 'score')

        d = dict(zip(df_largest['title'].to_list(), df_largest['score'].to_list()))
        if return_scores:
            return d
        else:
            return list(d.keys())