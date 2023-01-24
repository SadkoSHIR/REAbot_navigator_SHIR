import pandas as pd
from sklearn.ensemble import RandomForestClassifier

import csv


class Anketa:
    # static field
    data = []

    @staticmethod
    def create_anketa():
        file = open('data/anketa.csv', 'r')
        df = csv.reader(file, delimiter='#')
        for row in df:
            Anketa.data.append(row[0])
        file.close()

    @staticmethod
    def get_question(ind):
        if ind - 1 < len(Anketa.data):
            return Anketa.data[ind - 1]
        else:
            return ''

    @staticmethod
    def print_anketa():
        print(Anketa.data)


class RecommendModel:
    # static field
    model = RandomForestClassifier()

    @staticmethod
    def create_model():
        df = pd.read_csv('data/anchors2_utf8.csv',
                         sep=';',
                         header=0)
        df.head()
        X = df.drop(['q34', 'q33', 'q32'], axis=1)
        y = df['q34']

        # type(model)
        RecommendModel.model.fit(X, y)  # обучаем модель

    @staticmethod
    def get_recommendation(anketa):
        anketa_dic = {}
        for i in range(len(anketa)):
            anketa_dic[f'q{i + 1}'] = [anketa[i]]

        for i in range(len(anketa), 31):
            anketa_dic[f'q{i + 1}'] = [0]

        anketa_df = pd.DataFrame(anketa_dic)
        res = RecommendModel.model.predict(anketa_df)
        if len(res):
           return res[0]
        else:
           return ''

'''
# example of anketa
anketa = {'q1': [5],
 'q2': [9],
 'q3': [9],
 'q4': [5],
 'q5': [2],
 'q6': [1],
 'q7': [1],
 'q8': [3],
 'q9': [8],
 'q10': [4],
 'q11': [3],
 'q12': [1],
 'q13': [6],
 'q14': [2],
 'q15': [9],
 'q16': [4],
 'q17': [10],
 'q18': [8],
 'q19': [9],
 'q20': [1],
 'q21': [9],
 'q22': [10],
 'q23': [8],
 'q24': [1],
 'q25': [5],
 'q26': [3],
 'q27': [1],
 'q28': [8],
 'q29': [8],
 'q30': [6],
 'q31': [8]
 }


RecommendModel.create_model()
res = RecommendModel.get_recommendation([1,2,3,4,5,6,7,8,9,10])

print(res)

Anketa.create_anketa()
Anketa.print_anketa()
'''