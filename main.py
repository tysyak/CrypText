#!/usr/bin/env python3
#import json
import io
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Tweet import Tweet
from CryptoData import CryptoData
from datetime import datetime, timedelta
# from tqdm import tnrange, tqdm_notebook, tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


if __name__ == "__main__":
    # Cargar Datos
    tws = Tweet()
    tws.csv_tweet(tws.tweet(limit_tweet=100)) # gen csv in tmp/
    tf = glob.glob(f"./{tws.file_path}")
    dfs = []
    for file in tf:
        dfs.append(pd.read_csv(file))
    tweets = pd.concat(dfs)

    print('Tweets antes de soltar los duplicados.', tweets.shape)
    duplicates_removed = tweets.shape[0]
    tweets = tweets.drop_duplicates(subset=['Id'])
    duplicates_removed -= tweets.shape[0]
    print('Tweets después de soltar duplicados', tweets.shape)
    print('Duplicados eliminados ', duplicates_removed)

    # Display dataframes head
    tweets.head(2)
