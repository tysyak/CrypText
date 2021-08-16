#!/usr/bin/env python3
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Tweet import Tweet
from OptionParser import OptionParser
from CryptoData import CryptoData

def crosscorr(datax, datay, lag=0, method="pearson"):
    """Correlación Crusada"""
    return datax.corr(datay.shift(lag), method=method)



def main(opts):
    # Cargar Datos
    tws = Tweet()
    list_date =[
        ["2021-08-15","2021-08-16"],
        ["2021-08-14","2021-08-15"],
        ["2021-08-13","2021-08-14"],
        ["2021-08-12","2021-08-13"],
        ["2021-08-11","2021-08-12"]
    ]
    dfs = []
    query = '#BAT'
    lang = None
    lang = opts.lang
    if (opts.tweets is None):
        tws.file_path='tmp/tweet_work.csv'
        tws.csv_tweet(tws.get_interval_tweet(1500, list_date, query=query, lang=lang))
        dfs.append(pd.read_csv(tws.file_path))
    else:
        tws.file_path=opts.tweets
        dfs.append(pd.read_csv(opts.tweets))
    tweets = pd.concat(dfs)

    crd = CryptoData()
    crd_list = crd.csv_to_list()

    dfs = []
    dfs.append(pd.DataFrame(crd_list[1:], columns=crd_list[:1].pop()))
    crypto_pesos = pd.concat(dfs)
    crypto_pesos = crypto_pesos.sort_values(by=['Fecha'])

    tweets['CreatedAt'] = pd.to_datetime(tweets['CreatedAt'])
    tweets.index = tweets['CreatedAt']

    tweets_grouped = tweets.groupby(pd.Grouper(freq='1h'))['score'].sum()

    crypto_pesos['Fecha'] = pd.to_datetime(crypto_pesos['Fecha'], unit='s')
    crypto_pesos.index = crypto_pesos['Fecha']

    crypto_pesos_grouped = crypto_pesos.groupby(pd.Grouper(freq='1D'))['Cierre'].mean()
    
    _, ax1 = plt.subplots(figsize=(20,10))
    ax1.set_title("Evolución del BAT en comparación del sentimiento de Twitter", fontsize=18)
    ax1.tick_params(labelsize=14)
    ax2 = ax1.twinx()
    ax1.plot_date(tweets_grouped.index, tweets_grouped, 'g-')
    ax2.plot_date(crypto_pesos_grouped.index, crypto_pesos_grouped, 'b-')

    ax1.set_ylabel("Sentimiento", color='g', fontsize=16)
    ax2.set_ylabel("BAT [$]", color='b', fontsize=16)
    plt.savefig('1.evol_bat_vs_sent.png')
    if opts.plot:
        plt.show()

    beggining = max(tweets_grouped.index.min(), crypto_pesos_grouped.index.min())
    end = min(tweets_grouped.index.max(), crypto_pesos_grouped.index.max())
    tweets_grouped = tweets_grouped[beggining:end]
    crypto_pesos_grouped = crypto_pesos_grouped[beggining:end]

    _, ax1 = plt.subplots(figsize=(20,10))
    ax1.set_title("Evolución del BAT en comparación con el sentimiento de Twitter", fontsize=18)
    ax1.tick_params(labelsize=14)
    ax2 = ax1.twinx()
    ax1.plot_date(tweets_grouped.index, tweets_grouped, 'g-')
    ax2.plot_date(crypto_pesos_grouped.index, crypto_pesos_grouped, 'b-')

    ax1.set_ylabel("Sentimiento", color='g', fontsize=16)
    ax2.set_ylabel("BAT [$]", color='b', fontsize=16)
    plt.savefig('2.evol_bat_vs_sent.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="pearson") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("correlación cruzada de pearson")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('3.corr_pearson.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="kendall") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("correlación cruzada de kendall")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('4.corr_kendal.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="spearman") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("correlación cruzada de spearman")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('5.corr_spearman.png')
    if opts.plot:
        plt.show()

    tweets_grouped = tweets_grouped / max(tweets_grouped.max(), abs(tweets_grouped.min()))

    crypto_pesos_grouped = crypto_pesos_grouped / max(crypto_pesos_grouped.max(), abs(crypto_pesos_grouped.min()))
    fig, ax1 = plt.subplots(figsize=(20,10))
    ax1.set_title("Evolución normalizada del BAT en comparación con el sentimiento normalizado de Twitter", fontsize=18)
    ax1.tick_params(labelsize=14)

    ax2 = ax1.twinx()
    ax1.plot_date(tweets_grouped.index, tweets_grouped, 'g-')
    ax2.plot_date(crypto_pesos_grouped.index, crypto_pesos_grouped, 'b-')

    ax1.set_ylabel("Sentimiento", color='g', fontsize=16)
    ax2.set_ylabel("BAT normalizado", color='b', fontsize=16)
    plt.savefig('6.evol_bat_vs_sent_norm.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i) for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("impacto del retraso en la correlación (normalizado)")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('7.corr_impac_norm.png')
    if opts.plot:
        plt.show()

    tweets_grouped = pd.Series(np.gradient(tweets_grouped.values), tweets_grouped.index, name='slope')
    crypto_pesos_grouped = pd.Series(np.gradient(crypto_pesos_grouped.values), crypto_pesos_grouped.index, name='slope')

    _, ax1 = plt.subplots(figsize=(20,10))
    ax1.set_title("Derivada de la criptomoneda y la puntuación del sentimiento", fontsize=18)
    ax1.tick_params(labelsize=14)

    ax2 = ax1.twinx()
    ax1.plot_date(tweets_grouped.index, tweets_grouped, 'g-')
    ax2.plot_date(crypto_pesos_grouped.index, crypto_pesos_grouped, 'b-')

    ax1.set_ylabel("derivada del Sentimiento", color='g', fontsize=16)
    ax2.set_ylabel("derivada del BAT", color='b', fontsize=16)
    plt.savefig('8.dx_sent.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="pearson") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("pearson correlación cruzada (derivada)")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('9.dx_corr_pearson.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="kendall") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("kendall- Correlación Cruzada (derivada)")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('A.dx_corr_kendal.png')
    if opts.plot:
        plt.show()

    xcov = [crosscorr(tweets_grouped, crypto_pesos_grouped, lag=i, method="spearman") for i in range(-20,20)]
    plt.plot(range(-20,20), xcov)
    plt.title("spearman- Correlación Cruzada (derivada)")
    plt.xlabel("retraso")
    plt.ylabel("correlation")
    plt.savefig('B.dx_corr_spearman.png')
    if opts.plot:
        plt.show()




if __name__ == "__main__":
    argsv = OptionParser()
    opts = argsv.arguments()
    # print(opts.tweets is None)
    main(opts)
