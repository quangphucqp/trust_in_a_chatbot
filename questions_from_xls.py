import pandas as pd
import json


class QuestionsFromXls:
    def __init__(self):
        self.qna_df = self.load_files()

    def load_files(self):
        qna_df_dict = {}
        otree_qna_df = pd.read_excel('_static/questions_and_options/otree_qna_df.xlsx')

        # Load the sequence
        with open('_static/global/seq.json', 'r') as f:
            seq = json.load(f)

        for computer_number in seq:
            shuffled_indices = seq[computer_number]
            shuffled_qna_df = otree_qna_df.iloc[[i - 1 for i in shuffled_indices]].reset_index(drop=True)
            qna_df_dict[computer_number] = shuffled_qna_df

        return qna_df_dict
