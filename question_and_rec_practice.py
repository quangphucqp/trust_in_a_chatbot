import pandas as pd
import json


class QuestionsAndRecPractice:
    def __init__(self):
        self.qna_df, self.rec_df = self.load_files()  # assigning results of load_files to variables in one line

    def load_files(self):
        otree_qna_df = pd.read_excel('_static/practice/otree_qna_practice.xlsx')
        rec_df = pd.read_excel('_static/practice/static_practice.xlsx')
        return otree_qna_df, rec_df
