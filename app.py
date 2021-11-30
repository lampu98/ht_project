from numpy.core.fromnumeric import mean
import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re


#st.set_page_config(layout="centered")

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
        df_selected = pd.DataFrame(df[["departure", "alpha_3"]])
    else:
        df_selected = pd.DataFrame(df[["departure", "alpha_3"
                                       ]][df["arrival_1"] == option_arrival])

    data_map = pd.DataFrame(
        df_selected.groupby(["departure", "alpha_3"
                             ])["alpha_3"].agg(Victims="count")).reset_index()

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
        df_selected = pd.DataFrame(df[["arrival_1", "alpha_3"]])
    else:
        df_selected=pd.DataFrame(df[["arrival_1","alpha_3"]][df["departure"] == option_departure])

    data_map = pd.DataFrame(
        df_selected.groupby(["arrival_1", "alpha_3"
                             ])["alpha_3"].agg(Victims="count")).reset_index()

    fig = px.choropleth(data_map,
                        locations="alpha_3",
                        color="Victims",
                        hover_name="arrival_1",
                        color_continuous_scale='Viridis_r')
    fig.update_layout(title_text="Human Traffick countries of Destination")
    st.plotly_chart(fig)


#second graph

data_map = pd.read_csv(
    'gs://websitehumantrafficking/data_map.csv')


fig = px.choropleth(data_map,
                    locations="alpha_3",
                    color="Victims",
                    hover_name="country",
                    color_continuous_scale="Viridis_r",
                    width=600,
                    height=440)

fig.update_layout(title_text="Victim location from web scraping")

st.plotly_chart(fig)


#third graph
extracted_locations = pd.read_csv(
    'gs://websitehumantrafficking/extracted_locations.csv')
loc_data = extracted_locations['location'].value_counts().reset_index()
loc_data.rename(columns={
    'index': 'location',
    'location': 'count'
},
                inplace=True)
graph = loc_data.sort_values(by='count', ascending=False)
graphh = graph[graph["count"] > graph["count"].median()]
fig = px.bar(graph,
             x='location',
             y='count',
             hover_data=['location', 'count'],
             color='location')
st.plotly_chart(fig)


#fourth graph

all_age = [
    '0-8', '9-17', '18-20', '21-23', '24-26', '27-29', '30-38', '39-47', '48+'
]

col3, col4 = st.columns(2)

male_or_female = col3.radio('Select gender',
                                  ('male', 'female'))
option_age = col4.selectbox('Age', all_age)


scraped_data_only = df[0:1358]
moc_scraped = scraped_data_only.iloc[:, 9:26]
moc_scraped_data = pd.DataFrame(moc_scraped.sum(), columns=['sum'])



gen = df[df["gender"] == male_or_female].reset_index()
age_broad = gen[gen['ageBroad'] == option_age].reset_index()
MoC_data_bar = age_broad[(age_broad.meansOfControlConcatenated.notna())].\
meansOfControlConcatenated.apply(lambda x: pd.value_counts(str(x).split(";"))).sum(axis = 0)

means_of_control_top = MoC_data_bar.sort_values(ascending=False).head()
try:
    means_of_control_top.drop(labels="Not specified", inplace=True)
except:
    pass


means_of_control_top = means_of_control_top.reset_index()
means_of_control_top.rename(columns={"index": "Means of control",0:""}, inplace=True)

fig = px.histogram(means_of_control_top, x="Means of control", y="")
st.plotly_chart(fig)


#fifth graph
col5, col6 = st.columns(2)

all_age_third_graph = [
    '0-8', '9-17', '18-20', '21-23', '27-29', '24-26', '30-38', '39-47', '48+'
]

male_or_female_third_graph = col5.radio('Select gender', ('female', 'male'))
option_age_third_graph = col6.selectbox('Age', all_age_third_graph)

df_third_graph=df[df["gender"]==male_or_female_third_graph]
df_third_graph=df[df["ageBroad"]==option_age_third_graph]

HT_type1 = df_third_graph.filter(regex=("traf_type.*"))
HT_type2 = df_third_graph.filter(regex=("^is.*"))
HT_type = pd.concat([HT_type1, HT_type2], axis=1, join="outer")
HT_type.drop(columns = "traf_type_illegaladoption")
HT_type = HT_type.rename (columns = {"isSexualExploit": "Sexual", "isForcedLabour":"Forced labour", "isSexAndLabour": "Sex and labour", "isAbduction": "Abduction", "isSlaveryAndPractices": "Slavery and practices", "traf_type_domestic": "Domestic", "isForcedMarriage": "Forced marriage", "traf_type_cmarriage":"Forced marriage","traf_type_child":"Child abuse", "traf_type_fcriminality": "Forced criminality", "isForcedMilitary": "Forced military", "isOrganRemoval": "Organ removal", "traf_type_fpregnancy": "Forced pregnancy"} )
HT_type.drop(columns = ["traf_type_illegaladoption","isOtherExploit"], inplace = True)
HT_type_count = pd.DataFrame(HT_type.sum(), columns=["count"])
graph=HT_type_count.sort_values(by="count", ascending=False)
graph=graph.reset_index()
graph=graph[graph["count"]>graph["count"].median()]
graph.rename(columns = {"index": "Traffic type"}, inplace = True )

fig = px.histogram(graph, x="Traffic type", y = "count")
st.plotly_chart(fig)

#ngrams (sixth graph)
#ngram_1 = Image.open("img_1.png")
#ngram_2 = pd.read_csv('gs://websitehumantrafficking/img_2.png')
#ngram_3 = pd.read_csv('gs://websitehumantrafficking/img_3.png')
#ngram_4 = pd.read_csv('gs://websitehumantrafficking/img_4.png')
#ngram_5 = pd.read_csv('gs://websitehumantrafficking/img_5.png')
#ngram_6 = pd.read_csv('gs://websitehumantrafficking/img_6.png')
