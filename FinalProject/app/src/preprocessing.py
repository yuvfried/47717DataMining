import pandas as pd
from src.CONFIG import csv_filenames
from src.data_ingestion import BXReader

# read
reader = BXReader()
ratings = reader.get_data('ratings')
books = reader.get_data('books')
users = reader.get_data('users')

# pre-processing
# remove books which don't have meta-data
ratings = ratings.loc[ratings['ISBN'].isin(books['ISBN'])]
# remove observations which don't include rating
ratings = ratings.loc[ratings['Book-Rating']!=0]
ratings = ratings.rename(columns={"User-ID":"User","Book-Rating":"Rating"})

# we want to recommend about book title and not ISBN, for convinience of predicting new user
ratings.ISBN = ratings.ISBN.astype(str)
books.ISBN = books.ISBN.astype(str)
ratings = ratings.merge(books[['ISBN','Book-Title']], on='ISBN',how='inner')

