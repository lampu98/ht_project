import streamlit as st

import numpy as np
import pandas as pd

st.markdown("""#   What's in a survivor story?
""")

df = pd.read_csv("gs://websitehumantrafficking/final_df.csv")

option_departure = st.selectbox('Select the departure',
                                ('Vietnam', 'Mexico', 'Sri Lank'))
option_gender = st.selectbox('Select the gender', ("male", 'female'))

st.write(
    'Arrival_1:', df["arrival_1"][(df["departure"] == option_departure)
                                  & (df["gender"] == option_gender)])
