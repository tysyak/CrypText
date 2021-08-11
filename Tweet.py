#!/usr/bin/env python3

import tweepy as tw
import pandas as pd
from tqdm import tqdm
from os import getenv, path, remove

class Tweet:

    def __init__(self) -> None:
        self.file_path = 'tmp/tweets_to_work.csv'
        self._auth = tw.OAuthHandler(getenv('API_KEY'),
                                     getenv('API_KEY_SECRET'))
        self._api = tw.API(self._auth)
        self._auth.set_access_token(getenv('ACCESS_TOKEN'),
                                    getenv('ACCESS_TOKEN_SECRET'))

    def tweet(self, hashtag='#BAT', limit_tweet=100, lang="en") -> list:
        ret = [[
            'Id',
            'Text',
            'Username',
            'UserFollowerCount',
            'FavouritesCount',
            'CreatedAt'
        ]]
        with tqdm(total=limit_tweet) as pbar:
            for tweet in tqdm(
                    tw.Cursor(self._api.search, lang=lang, q=hashtag, rpp=100).items(limit_tweet),
                    ascii=True, desc="Obteniendo Tweets"):
                ret.append([
                    str(tweet.id),
                    tweet.text,
                    tweet.user.name,
                    tweet.user.followers_count,
                    tweet.user.favourites_count,
                    tweet.created_at
                ])
                pbar.update(1)
        return ret

    def csv_tweet(self, list_to_convert, file_path='tmp/tweets_to_work.csv') -> None:
        df = pd.DataFrame(list_to_convert)
        if path.exists(file_path):
            remove(file_path)
        df.to_csv(file_path, index=False, header=False)


if __name__ == '__main__':
    tws = Tweet()
    tws.csv_tweet(tws.tweet(limit_tweet=100))
