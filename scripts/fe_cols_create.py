import sys
sys.path.append('../')

import pandas as pd

import nlp_utils

TERMS_JSON = '../age_dicts/terms.json'
TEXT_FILENAME = 'INSERT_CSV.csv'

df = pd.read_csv(TEXT_FILENAME, delimiter = ',' , encoding = 'unicode_escape')

df['text'] = df['text'].astype('str')

df = nlp_utils.add_wordlist_cols(df, text_col='text', terms_json=TERMS_JSON)

df.to_csv("raw_data/feature_eng_df.csv")
