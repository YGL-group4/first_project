# coding=utf-8
"""
-----------------------------------------------------------------------------------
메인 함수

# Description:
1.
2.
3.
4.
5.

-----------------------------------------------------------------------------------
"""

from MiniProject1.src.config import folder
from MiniProject1.src.data_process import summoners
from MiniProject1.src.data_process import crawling
from MiniProject1.src.data_process import formatter
from MiniProject1.src.model import modeling

import pandas as pd


class MainFunction():

    def __init__(self):
        self.data = None
        self.modeling = None
        self.score = None

    # 1. make data
    def make_data(self):
        """
        학습할 데이터를 생성한다.
        """
        ################## fill in the code  ###################
        # df_summoners = summoners.get_summoners_list()
        # df_data = crawling.get_data(df_summoners)

        # df_data.to_csv('data_name.csv')
        ########################################################

    # 2. get data
    def get_data(self):
        """
        data를 가져옴
        :return: loaded data
        """
        path = folder.get_data_path('challenger_0521.csv')
        data = pd.read_csv(path, index_col=0)

        data = formatter.longer_playtime(data, '20:00')

        # get only mid position
        data = data[data['position'] == 'mid']
        data = data.drop(['position'], axis=1)

        self.data = data

    # 3. create and train, test model
    def train_test_model(self):
        x_train, y_train, x_test, y_test = formatter.split_data(self.data)

        LR = modeling.LogReg()
        x_train = LR.scale_input_data(x_train)
        LR.train(x_train, y_train)
        LR.get_score(x_train, y_train)

        x_test = LR.scale_input_data(x_test)
        LR.get_score(x_test, y_test)

        self.modeling = LR

    # 4. evaluate model
    def evaluate_model(self):
        from MiniProject1.src.data_process import summoners
        from MiniProject1.src.data_process import crawling

        name = '탈론의신탈론의왕'
        df_summoners = summoners.get_summoner_df(name)
        poro = crawling.PoroCrawling1(df_summoners)
        data = poro.data

        # 20분 이상, mid 포지션만 남김
        data = formatter.longer_playtime(data, '20:00')
        data = data[data['position'] == 'mid']
        data = data.drop(['position'], axis=1)

        LR = self.modeling
        x, y = formatter.split_input_output(data)
        x = LR.scale_input_data(x)
        LR.get_score(x, y)


if __name__ == '__main__':

    func = MainFunction()
    func.get_data()
    func.train_test_model()
    func.evaluate_model()