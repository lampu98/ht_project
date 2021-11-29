import streamlit as st

import numpy as np
import pandas as pd

import pandas as pd
import plotly.express as px

all_departure = [
    'Select all','Vietnam', 'Sri Lanka', 'Mexico', 'Sudan', 'Cameroon', 'United States',
    'Haiti', 'India', 'Mauritania', 'Too much countries', 'Niger', 'China',
    'Mali', 'Iraq', 'Nigeria', 'Zimbabwe', 'Indonesia', 'Kenya', 'Philippines',
    'North Korea', 'Cambodia', 'Togo', 'Ukraine', 'Albania', 'Egypt',
    'United Kingdom', 'Spain', 'Romania', 'Hungary', 'Sierra Leone', 'Ecuador',
    'Dominican Republic', 'Honduras', 'South Africa', 'Ireland',
    'Lithuania', 'Brazil', 'Ghana', 'Nepal', 'Czech Republic', 'Guinea',
    'Tanzania', 'Bangladesh', 'Colombia', 'Senegal', 'Malaysia', 'Laos',
    'Afghanistan', 'Croatia', 'Uganda', 'Rwanda', 'Canada', 'Poland', 'Sweden',
    'Libya', 'Russia', 'Thailand', 'Armenia', 'Peru', 'Germany', 'Venezuela',
    'Israel', 'Moldova', 'Zambia', 'Slovakia', 'Belarus', 'Malawi', 'Qatar',
    'Yemen', 'Kyrgyzstan', 'Uzbekistan', 'Syria', 'Burundi', 'Ethiopia',
    'Guatemala', 'Chad', 'Tunisia', 'Pakistan', 'Eritrea', 'Turkey', 'Fiji',
    'Burma', 'Lesotho', 'Belgium', 'Benin', 'United Arab Emirates',
    'Kazakhstan', 'Azerbaijan', 'Slovenia', 'Somalia', 'Moldova, Republic of',
    'Bulgaria', 'Tajikistan', 'Congo, The Democratic Republic of the',
    'Guinea-Bissau', "Côte d'Ivoire", 'Myanmar',
    "Lao People's Democratic Republic", 'Turkmenistan', 'Burkina Faso',
    'Bolivia, Plurinational State of', 'Viet Nam', 'Korea, Republic of',
    'El Salvador', 'Madagascar', 'Jamaica', 'Micronesia, Federated States of',
    'Mongolia', 'Russian Federation', 'Cuba'
]
all_arrival = [
    'Select all', 'American Samoa', 'Lebanon', 'India', 'United States',
    'Sudan', 'Haiti', 'Mauritania', 'Too much countries', 'Niger', 'China',
    'France', 'Mexico', 'United Kingdom', 'Iraq', 'Netherlands',
    'South Africa', 'Kenya', 'North Korea', 'Cambodia', 'Ghana', 'Thailand',
    'United Arab Emirates', 'Afghanistan', 'Ireland', 'Brazil', 'Italy',
    'Qatar', 'Malaysia', 'Singapore', 'Honduras', 'Australia', 'Peru', 'Nepal',
    'Russia', 'Philippines', 'Pakistan', 'Tanzania', 'Oman', 'Sierra Leone',
    'Nigeria', 'Japan', 'Uganda', 'Bangladesh', 'Malawi', 'Cameroon',
    'Senegal', 'Indonesia', 'Vietnam', 'Moldova', 'Israel', 'Rwanda',
    'Ethiopia', 'Canada', 'Lithuania', 'Kuwait', 'Belgium', 'Libya', 'Serbia',
    'Egypt', 'Liberia', 'Greece', 'Saudi Arabia', 'Uzbekistan', 'Germany',
    'Slovenia', 'Albania', 'Venezuela', 'Turkey', 'Colombia', 'Ukraine',
    'Bahrain', 'Burundi', 'Fiji', 'Spain', 'Romania', 'Hong Kong', 'Benin',
    'Gabon', 'Jordan', 'Eritrea', 'Yemen', 'Kyrgyzstan', 'Syria', 'Guatemala',
    'Chad', 'Tunisia', 'Cyprus', 'Taiwan', 'Lesotho', 'Zimbabwe',
    'Bosnia and Herzegovina', 'North Macedonia', 'Russian Federation',
    'Bulgaria', 'Poland', 'Tajikistan', 'Czechia', 'Austria', 'Kazakhstan',
    'Ecuador', 'Turkmenistan', 'Tanzania, United Republic of', 'Argentina',
    'Morocco', 'Syrian Arab Republic', 'Taiwan, Province of China',
    'Trinidad and Tobago', 'Belarus', 'Denmark', 'Mauritius', 'Viet Nam',
    "Côte d'Ivoire", 'Sweden', 'Mali', 'Madagascar', 'Vanuatu', 'Chile'
]

st.markdown("""#   What's in a survivor story?
""")

df = pd.read_csv("gs://websitehumantrafficking/final_df.csv")

col1, col2= st.columns(2)


arrival_or_departure = col1.radio('Select country of', ('Origin', 'Destination'))


if arrival_or_departure == 'Destination':
    option_arrival = col2.selectbox('', all_arrival)
    if option_arrival == "Select all":
        df = pd.DataFrame(df[["departure", "alpha_3"]])
    else:
        df = pd.DataFrame(df[["departure",
                              "alpha_3"]][df["arrival_1"] == option_arrival])

    data_map = pd.DataFrame(
        df.groupby(["departure",
                    "alpha_3"])["alpha_3"].agg(Victims="count")).reset_index()

    fig = px.choropleth(data_map,
                        locations="alpha_3",
                        color="Victims",
                        hover_name="departure",
                        color_continuous_scale='Viridis_r')
    fig.update_layout(title_text="Human Traffick countries of Origin")
    st.plotly_chart(fig)

elif arrival_or_departure == 'Origin':
    option_departure = col2.selectbox('', all_departure)
    if option_departure == "Select all":
        df = pd.DataFrame(df[["arrival_1",
                            "alpha_3"]])
    else:
        df=pd.DataFrame(df[["arrival_1","alpha_3"]][df["departure"] == option_departure])

    data_map = pd.DataFrame(
        df.groupby(["arrival_1",
                    "alpha_3"])["alpha_3"].agg(Victims="count")).reset_index()

    fig = px.choropleth(data_map,
                        locations="alpha_3",
                        color="Victims",
                        hover_name="arrival_1",
                        color_continuous_scale='Viridis_r')
    fig.update_layout(title_text="Human Traffick countries of Destination")
    st.plotly_chart(fig)
