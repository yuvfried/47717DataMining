from src.CONFIG import csv_filenames
import pandas as pd
import numpy as np


class BXReader:

    def __init__(self, d_conf=csv_filenames):
        self.d_conf = d_conf
        self.d_names = self.d_conf.keys()

    def read_to_df(self, filename):
        return pd.read_csv(filename, delimiter=';', error_bad_lines=False, encoding='latin-1')

    def get_data(self, name):
        return self.read_to_df(self.d_conf[name])

