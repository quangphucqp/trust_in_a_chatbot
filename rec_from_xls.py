import os
import pandas as pd


class RecFromXls:
    def __init__(self):
        self.rec_df = self.load_files()

    def load_files(self):
        data_dir = '_static/static_recommendations'

        # list comprehension to get all .xls files in the directory
        file_names = [file_name for file_name in os.listdir(data_dir) if 'xls' in file_name]

        rec_df_dict = {}

        for file_name in file_names:
            file_path = os.path.join(data_dir, file_name)

            # Extracting the computer_number
            computer_number = int(''.join(filter(str.isdigit, file_name.split('_')[1])))
            # Reading the file using pandas
            df = pd.read_excel(file_path)

            rec_df_dict[computer_number] = df

        return rec_df_dict
