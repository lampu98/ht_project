import sys
sys.path.append('../')

import pandas as pd

from ht_project import nlp_utils

TERMS_JSON = 'data/fe_dicts.json'
TEXT_FILENAME = 'raw_data/final_dataframe.csv'

#TO DO: should output ones and zeros instead of matches

df = pd.read_csv(TEXT_FILENAME, delimiter = ',' , encoding = 'unicode_escape')

df['text'] = df['text'].astype('str')

df = nlp_utils.add_wordlist_cols(df, text_col='text', terms_json=TERMS_JSON)

df.to_csv("raw_data/feature_eng_df.csv")
