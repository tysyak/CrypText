#!/usr/bin/env python3

import tweepy as tw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from tqdm import tqdm
from os import getenv, path, remove

class Tweet:

    def __init__(self) -> None:
        self.file_path = 'tmp/tweets_to_work.csv'
        self._auth = tw.OAuthHandler(
            getenv('API_KEY'),
            getenv('API_KEY_SECRET')
        )
        self._api = tw.API(self._auth)
        self._auth.set_access_token(
            getenv('ACCESS_TOKEN'),
            getenv('ACCESS_TOKEN_SECRET')
        )

    def tweet(self, hashtag='#BAT',
              limit_tweet=100, lang="en") -> list:
        ret = [[
            'Id',
            'Text',
            'Username',
            'UserFollowerCount',
            'FavouritesCount',
            'CreatedAt',
            'score' # TODO
        ]]

        analyzer = SentimentIntensityAnalyzer()
        with tqdm(total=limit_tweet) as pbar:
            for tweet in tqdm(
                    tw.Cursor(self._api.search,
                              lang=lang,
                              q=hashtag,
                              rpp=100)
                    .items(limit_tweet),
                    ascii=True,
                    desc="Obteniendo Tweets"):
                ret.append([
                    str(tweet.id),
                    tweet.text,
                    tweet.user.name,
                    tweet.user.followers_count,
                    tweet.user.favourites_count,
                    tweet.created_at,
                    analyzer.polarity_scores(
                        tweet.text
                    )['compound'] * (
                        (tweet.user.followers_count + 1) *
                        (tweet.favorite_count + 1))
                ])
                pbar.update(1)
        return ret

    def csv_tweet(self, list_to_convert) -> None:
        df = pd.DataFrame(list_to_convert)
        if path.exists(self.file_path):
            remove(self.file_path)
        print("guardado en " + self.file_path)
        df.to_csv(self.file_path, index=False, header=False)

    def get_interval_tweet(self,
                           limit_tweet,
                           interval_date_list,
                           query='#BAT',
                           lang='es'):
        ret = [[
            'Id',
            'Text',
            'Username',
            'UserFollowerCount',
            'FavouritesCount',
            'CreatedAt',
            'score'
        ]]
        i=0
        for interval in interval_date_list:
            analyzer = SentimentIntensityAnalyzer()
            for tweet in tw.Cursor(
                    self._api.search,
                    lang=lang,
                    q=query,
                    rpp=100,
                    tweet_mode='extended',
                    # result_type='mixed',
                    since=interval[0],
                    until=interval[1])\
                           .items(limit_tweet):
                ana = analyzer.polarity_scores(tweet.full_text)
                score = ana['compound'] * (
                        (tweet.user.followers_count + 1) *
                        (tweet.favorite_count + 1))
                ret.append([
                    str(tweet.id),
                    tweet.full_text,
                    tweet.user.name,
                    tweet.user.followers_count,
                    tweet.user.favourites_count,
                    tweet.created_at,
                    score
                ])
                i = i+1
            print(interval[0]+'-'+interval[0]+': ' + str(i))
        return ret

        


if __name__ == '__main__':
    tws = Tweet()
    tws.file_path='tmp/tweet_work.csv'
    # tws.csv_tweet(tws.tweet(limit_tweet=100))
    list_date =[
        ["2021-08-12","2021-08-13"],
        ["2021-08-11","2021-08-12"],
        ["2021-08-10","2021-08-11"],
        ["2021-08-09","2021-08-10"],
        ["2021-08-08","2021-08-09"],
        # ["2021-08-07","2021-08-08"]
    ]
    tws.file_path='tmp/tweet_work.csv'
    tws.csv_tweet(
        tws.get_interval_tweet(
            100, list_date, query='#BAT', lang='es'
        )
    )
