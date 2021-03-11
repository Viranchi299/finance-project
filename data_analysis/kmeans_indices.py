#imports
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
import numpy as np
from scipy.cluster.vq import kmeans,vq
import pandas as pd
import pandas_datareader as dr
from math import sqrt
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sqlalchemy import create_engine


def kmeans_index(index):
    if index not in {'sp500', 'nasdaq100', 'russell1000'}:
        return None
    else:
        # get_table = f'sqlite:///{index}.db'
        engine = create_engine('sqlite:///indices_data')
        engine.connect()
        print('Tables: ', engine.table_names('main'))
        data = pd.read_sql_table(f'{index}', engine)
    print(data)

def run_kmeans(index_data):
    pass


if __name__ == '__main__':
    print('starting')
    kmeans_index('sp500')
