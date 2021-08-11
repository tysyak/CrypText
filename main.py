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
    dfs = []
    dfs.append(pd.read_csv(tws.file_path))
    tweets = pd.concat(dfs)

    print('Tweets antes de soltar los duplicados.', tweets.shape)
    duplicates_removed = tweets.shape[0]
    tweets = tweets.drop_duplicates(subset=['Id'])
    duplicates_removed -= tweets.shape[0]
    print('Tweets después de soltar duplicados', tweets.shape)
    print('Duplicados eliminados ', duplicates_removed)

    # Display dataframes head
    # print(tweets.head(2))

    crd = CryptoData()
    crd_list = crd.csv_to_list()

    dfs = []
    dfs.append(pd.DataFrame(crd_list[1:], columns=crd_list[:1].pop()))
    crypto_pesos = pd.concat(dfs)
    crypto_pesos = crypto_pesos.sort_values(by=['Fecha'])

    print('bitcoin shape before droping duplicates', crypto_pesos.shape)
    duplicates_removed = crypto_pesos.shape[0]
    crypto_pesos = crypto_pesos.drop_duplicates(subset=['Fecha'])
    print('bitcoin shape after droping duplicates', crypto_pesos.shape)
    duplicates_removed -= crypto_pesos.shape[0]
    print('duplicates removed', duplicates_removed)

    tweets['CreatedAt'] = pd.to_datetime(tweets['CreatedAt'])
    tweets.index = tweets['CreatedAt']

    tweets_grouped = tweets.groupby(pd.Grouper(freq='1h'))['score'].sum()

    crypto_pesos['Fecha'] = pd.to_datetime(crypto_pesos['Fecha'], unit='s')
    crypto_pesos.index = crypto_pesos['Fecha']

    crypto_pesos_grouped = crypto_pesos.groupby(pd.Grouper(freq='1h'))['Cierre'].mean()

    fig, ax1 = plt.subplots(figsize=(20,10))
    ax1.set_title("Crypto currency evolution compared to twitter sentiment", fontsize=18)
    ax1.tick_params(labelsize=14)
    ax2 = ax1.twinx()
    ax1.plot_date(tweets_grouped.index, tweets_grouped, 'g-')
    ax2.plot_date(crypto_pesos_grouped.index, crypto_pesos_grouped, 'b-')

    ax1.set_ylabel("Sentiment", color='g', fontsize=16)
    ax2.set_ylabel("BAT [$]", color='b', fontsize=16)
    plt.show()
