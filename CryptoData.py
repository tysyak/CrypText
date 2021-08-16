#!/usr/bin/env python3

import time
import pandas as pd

class CryptoData:
    def __init__(self) -> None:
        self.csv_list = list()

    def csv_to_list(self, csv_path='tmp/bat-mxn-max.csv') -> list:
        df = pd.read_csv(csv_path, delimiter=',')
        self.csv_list = [list(row) for row in df.values]
        self.csv_list.insert(0, df.columns.to_list())
        self._time_to_timestamp()
        return self.csv_list

    def _time_to_timestamp(self):
        for i in range(1,len(self.csv_list)):
            self.csv_list[i][0] = int(time.mktime(
                time.strptime(self.csv_list[i][0], '%d.%m.%Y')))



if __name__ == '__main__':
    some = CryptoData()
    print(some.csv_to_list())
