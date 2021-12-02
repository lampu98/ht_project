from numpy.core.fromnumeric import mean
import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
import joblib


#st.set_page_config(layout="centered")
#st.set_page_config(page_title="Human Trafficking", page_icon="🖖")

all_departure = ["Select all",'Afghanistan', 'Albania', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Belarus', 'Belgium', 'Benin', 'Bolivia, Plurinational State of', 'Brazil', 'Bulgaria',
                 'Burkina Faso', 'Burma', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Chad', 'China', 'Colombia', 'Congo, The Democratic Republic of the', 'Croatia', 'Cuba', 'Czech Republic',
                 "Côte d'Ivoire", 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea', 'Ethiopia', 'Fiji', 'Germany', 'Ghana', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Haiti',
                 'Honduras', 'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Jamaica', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic",
                 'Laos', 'Lesotho', 'Libya', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mexico', 'Micronesia, Federated States of', 'Moldova', 'Moldova, Republic of',
                 'Mongolia', 'Myanmar', 'Nepal', 'Niger', 'Nigeria', 'North Korea', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Qatar', 'Romania', 'Russia', 'Russian Federation', 'Rwanda', 'Senegal',
                 'Sierra Leone', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Too much countries',
                 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uzbekistan', 'Venezuela', 'Viet Nam', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
all_arrival = [
    'Select all', 'Afghanistan', 'Albania', 'American Samoa', 'Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Benin',
    'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Chad', 'Chile', 'China', 'Colombia', 'Cyprus', 'Czechia',
    "Côte d'Ivoire", 'Denmark', 'Ecuador', 'Egypt', 'Eritrea', 'Ethiopia', 'Fiji', 'France', 'Gabon', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Haiti',
    'Honduras', 'Hong Kong', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan',
    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova',
    'Morocco', 'Nepal', 'Netherlands', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Oman', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Qatar',
    'Romania', 'Russia', 'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Singapore', 'Slovenia', 'South Africa',
    'Spain', 'Sudan', 'Sweden', 'Syria', 'Syrian Arab Republic', 'Taiwan', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania', 'Tanzania, United Republic of',
    'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States',
    'Uzbekistan', 'Vanuatu', 'Venezuela', 'Viet Nam', 'Vietnam', 'Yemen', 'Zimbabwe']


st.markdown("""#   What's in a survivor story?
""")

st.markdown(
    """ #### By using NLP to extract key intelligence from survivor testimonies, and by combining this with existing datasets on human trafficking, this project aims to show that data science can:
 1. Enrich the currently sparse global picture of human trafficking by allowing the collection of data that would be too cumbersome/costly to collect manually
 2. Aid data interpretation, finding patterns that would perhaps be overlooked if assessed by humans alone
 3. Encourage more organisations to share their data, even if it is unstructured,  by showing the richness of information that can be obtained from each survivor story, and highlighting the value of this information to disruption efforts
    """
)

st.markdown("#")
st.markdown("#")

df = pd.read_csv("gs://websitehumantrafficking/final_small_df.csv")

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
    fig.update_layout(
        title_text=
        "Countries of Origin based on web scraped metadata combined with CTDC data"
    )
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
    fig.update_layout(
        title_text=
        "Countries of Destination based on web scraped metadata combined with CTDC data"
    )
    st.plotly_chart(fig)


#second graph

data_map = pd.read_csv(
    'gs://websitehumantrafficking/data_map.csv')


fig = px.choropleth(data_map,
                    locations="alpha_3",
                    color="Victims",
                    hover_name="country",
                    color_continuous_scale="Viridis_r",
                    )

fig.update_layout(
    title_text=
    "Map showing locations extracted from survivor testimonies using Named Entity Recognition",
    showlegend=False)

st.plotly_chart(fig)


#third graph
extracted_locations = pd.read_csv(
    'gs://websitehumantrafficking/extracted_locations.csv')
loc_data = extracted_locations['location'].value_counts()[:30].reset_index()
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

fig.update_layout(
    title_text=
    "Most commonly cited locations in the survivor testimonies, extracted with NER",
    showlegend=False)
st.plotly_chart(fig)

st.markdown("#")

#fourth graph
gender_age_df = pd.read_csv('gs://websitehumantrafficking/gender_age_df.csv')
fig = px.sunburst(gender_age_df[gender_age_df.ageBroad.notna()],
                  path=['gender', 'ageBroad'],
                  values='Victims',
                  color='gender',
                  color_discrete_map={'female':'pink', 'male':'light blue'},
                  title='Gender and Age of Human Trafficking Victims')
fig.update_layout(showlegend=False)
st.plotly_chart(fig)
st.markdown("#")

#fifth graph

all_age = [
    '0-8', '9-17', '18-20', '21-23', '24-26', '27-29', '30-38', '39-47', '48+'
]

st.markdown("""
            ##### Select age and gender of  victim the to see the main means of control used
            """)

col3, col4 = st.columns(2)

male_or_female = col3.radio('Gender',
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

fig = px.bar(means_of_control_top,
             x="Means of control",
             y="",
             color='Means of control'
             )
fig.update_layout(showlegend=False)
st.plotly_chart(fig)

st.markdown("#")
st.markdown("#")
#sixth graph

st.markdown("""
            ##### Select age and gender to see the most common exploitation types
            """)

col5, col6 = st.columns(2)

all_age_third_graph = [
    '0-8', '9-17', '18-20', '21-23', '27-29', '24-26', '30-38', '39-47', '48+'
]

male_or_female_third_graph = col5.radio('Gender', ('female', 'male'))
option_age_third_graph = col6.selectbox('Age', all_age_third_graph)

df_third_graph=df[df["gender"]==male_or_female_third_graph]
df_third_graph=df[df["ageBroad"]==option_age_third_graph]

HT_type1 = df_third_graph.filter(regex=("traf_type.*"))
HT_type2 = df_third_graph.filter(regex=("^is.*"))
HT_type = pd.concat([HT_type1, HT_type2], axis=1, join="outer")
HT_type.drop(columns = "traf_type_illegaladoption")
HT_type = HT_type.rename(columns = {"isSexualExploit": "Sexual", "isForcedLabour":"Forced labour", "isSexAndLabour": "Sex and labour", "isAbduction": "Abduction", "isSlaveryAndPractices": "Slavery and practices", "traf_type_domestic": "Domestic", "isForcedMarriage": "Forced marriage", "traf_type_cmarriage":"Forced marriage","traf_type_child":"Child abuse", "traf_type_fcriminality": "Forced criminality", "isForcedMilitary": "Forced military", "isOrganRemoval": "Organ removal", "traf_type_fpregnancy": "Forced pregnancy"} )
HT_type.drop(columns = ["traf_type_illegaladoption","Abduction","isOtherExploit"], inplace = True)
HT_type_count = pd.DataFrame(HT_type.sum(), columns=["count"])
graph=HT_type_count.sort_values(by="count", ascending=False)
graph=graph.reset_index()
graph=graph[graph["count"]>graph["count"].median()]
graph.rename(columns = {"index": "Trafficking type"}, inplace = True )

fig = px.bar(graph,
             x="Trafficking type",
             y = "count",
             color="Trafficking type")
fig.update_layout(showlegend=False)
st.plotly_chart(fig)

st.markdown("#")
st.markdown("#")
#seventh graph
all_destination_country = [
    "Select all",'Afghanistan', 'Albania', 'American Samoa', 'Argentina', 'Australia',
    'Austria', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Benin',
    'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia',
    'Cameroon', 'Canada', 'Chad', 'Chile', 'China', 'Colombia', 'Cyprus',
    'Czechia', "Côte d'Ivoire", 'Denmark', 'Ecuador', 'Egypt', 'Eritrea',
    'Ethiopia', 'Fiji', 'France', 'Gabon', 'Germany', 'Ghana', 'Greece',
    'Guatemala', 'Haiti', 'Honduras', 'Hong Kong', 'India', 'Indonesia',
    'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan',
    'Kenya', 'Kuwait', 'Kyrgyzstan', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
    'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania',
    'Mauritius', 'Mexico', 'Moldova', 'Morocco', 'Nepal', 'Netherlands',
    'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Oman', 'Pakistan',
    'Peru', 'Philippines', 'Poland', 'Qatar', 'Romania', 'Russia',
    'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia',
    'Sierra Leone', 'Singapore', 'Slovenia', 'South Africa', 'Spain', 'Sudan',
    'Sweden', 'Syria', 'Syrian Arab Republic', 'Taiwan',
    'Taiwan, Province of China', 'Tajikistan', 'Tanzania',
    'Tanzania, United Republic of', 'Thailand',
    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States',
    'Uzbekistan', 'Vanuatu', 'Venezuela', 'Viet Nam', 'Vietnam', 'Yemen',
    'Zimbabwe'
]
st.markdown("""
            ##### Select a country to see the main industries of exploitation
    """)


option_destination_country = st.selectbox('Destination', all_destination_country)

if option_destination_country=="Select all":
    df_traf_industry = df
    traf_industry1 = df_traf_industry.filter(regex=("traf_industry.*"))
    traf_industry2 = df_traf_industry.filter(regex=("typeOfLabour.*"))
    traf_industry = pd.concat([traf_industry1, traf_industry2],
                              axis=1,
                              join="outer")
    traf_industry.drop(
        columns=['typeOfLabourNotSpecified', 'typeOfLabourOther'],
        inplace=True)
    traf_industry.rename(columns={
        'typeOfLabourDomesticWork': 'Domestic work',
        'typeOfLabourAgriculture': 'Agriculture',
        'typeOfLabourConstruction': 'Construction',
        'typeOfLabourManufacturing': 'Manufacturing',
        'typeOfLabourHospitality': 'Hospitality',
        'typeOfLabourIllicitActivities': 'Activities',
        'typeOfLabourBegging': 'Begging',
        'typeOfLabourAquafarming': 'Aquafarming',
        'typeOfLabourPeddling': 'Peddling',
        'traf_industry_clothes_manufacturing': 'Clothes manufacturing',
        'typeOfLabourMiningOrDrilling': 'Mining',
        'typeOfLabourTransportation': 'Transportation',
        'traf_industry_sexualservitude': 'Sexual servitude',
        'traf_industry_cleaning': 'Cleaning',
        'traf_industry_benefitfraud': 'Benefit fraud',
        'traf_industry_retail': 'Retail'
    },
                         inplace=True)
    traf_industry_count = pd.DataFrame(traf_industry.sum(), columns=['count'])
    traf_industry_count.sort_values(by='count', ascending=False)
    traf_industry_count.reset_index(inplace=True)
    traf_industry_count.rename(columns={'index': 'Trafficking industry'},
                               inplace=True)
    traf_graph = traf_industry_count.sort_values(by='count', ascending=False)
    traf_graph = traf_graph[traf_graph["count"] > traf_graph["count"].median()]

    fig = px.bar(traf_graph,
                 x="Trafficking industry",
                 y='count',
                 hover_data=['Trafficking industry', 'count'],
                 color='Trafficking industry')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

else:
    df_traf_industry = df[df["arrival_1"] == option_destination_country]
    traf_industry1 = df_traf_industry.filter(regex=("traf_industry.*"))
    traf_industry2 = df_traf_industry.filter(regex=("typeOfLabour.*"))
    traf_industry = pd.concat([traf_industry1, traf_industry2], axis=1, join="outer")
    traf_industry.drop(columns = ['typeOfLabourNotSpecified','typeOfLabourOther'], inplace = True)
    traf_industry.rename(columns = {'typeOfLabourDomesticWork': 'Domestic work', 'typeOfLabourAgriculture':'Agriculture', 'typeOfLabourConstruction': 'Construction', 'typeOfLabourManufacturing': 'Manufacturing', 'typeOfLabourHospitality': 'Hospitality', 'typeOfLabourIllicitActivities': 'Activities', 'typeOfLabourBegging': 'Begging', 'typeOfLabourAquafarming':'Aquafarming','typeOfLabourPeddling':'Peddling', 'traf_industry_clothes_manufacturing': 'Clothes manufacturing', 'typeOfLabourMiningOrDrilling': 'Mining', 'typeOfLabourTransportation': 'Transportation', 'traf_industry_sexualservitude': 'Sexual servitude', 'traf_industry_cleaning': 'Cleaning', 'traf_industry_benefitfraud': 'Benefit fraud', 'traf_industry_retail': 'Retail'}, inplace = True)
    traf_industry_count = pd.DataFrame(traf_industry.sum(), columns=['count'])
    traf_industry_count.sort_values(by='count', ascending=False)
    traf_industry_count.reset_index(inplace = True)
    traf_industry_count.rename(columns={'index': 'Trafficking industry'},
                               inplace=True)
    traf_graph=traf_industry_count.sort_values(by='count', ascending=False)
    traf_graph=traf_graph[traf_graph["count"]>traf_graph["count"].median()]

    fig = px.bar(traf_graph,
                 x="Trafficking industry",
                 y='count',
                 hover_data=['Trafficking industry', 'count'],
                 color='Trafficking industry')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

st.markdown("#")
st.markdown("#")
#eigth graph

st.markdown("""
            ##### Cases recorded in a given year in each country in the combined dataset
    """)

fig = pd.pivot_table(df,
                       values='Datasource',
                       index='arrival_1',
                       columns='year',
                       aggfunc='count',
                       fill_value=0)

cm = sns.light_palette("red", as_cmap=True)

st.write(fig.style.background_gradient(cmap=cm))

st.markdown("#")
st.markdown("#")
st.markdown("#")
st.markdown("#")
st.markdown("#")
#ninth grapgh (model)

gender_X_model=["female","male"]
departure_X_model=['Afghanistan', 'Albania', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Belarus', 'Belgium', 'Benin', 'Bolivia, Plurinational State of', 'Brazil', 'Bulgaria',
                 'Burkina Faso', 'Burma', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Chad', 'China', 'Colombia', 'Congo, The Democratic Republic of the', 'Croatia', 'Cuba', 'Czech Republic',
                 "Côte d'Ivoire", 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea', 'Ethiopia', 'Fiji', 'Germany', 'Ghana', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Haiti',
                 'Honduras', 'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Jamaica', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic",
                 'Laos', 'Lesotho', 'Libya', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mexico', 'Micronesia, Federated States of', 'Moldova', 'Moldova, Republic of',
                 'Mongolia', 'Myanmar', 'Nepal', 'Niger', 'Nigeria', 'North Korea', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Qatar', 'Romania', 'Russia', 'Russian Federation', 'Rwanda', 'Senegal',
                 'Sierra Leone', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Too much countries',
                 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uzbekistan', 'Venezuela', 'Viet Nam', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
age_model_X=[
    '9-17', '0-8', '18-20', '21-23', '24-26', '27-29', '30-38', '39-47', '48+'
]

st.markdown(
    "### Likelihood of a person of being subject to forced labour type based on age, gender and country of origin"
)

gender_model_column_1,departure_model_column_1,age_model_column_1=st.columns(3)

gender_selection_model_1=gender_model_column_1.selectbox('Gender', gender_X_model)
departure_selection_model_1=departure_model_column_1=departure_model_column_1.selectbox('Departure', departure_X_model)
age_selection_model_1=age_model_column_1=age_model_column_1.selectbox('Age', age_model_X)

my_X = [
    gender_selection_model_1,
    departure_selection_model_1,
    age_selection_model_1
]

model_ForcedLabour = joblib.load('test_IsForcedLabour.joblib')
prediction = model_ForcedLabour.predict([my_X])[0]

if prediction==0:
    st.markdown(
        "#### Based on your selection, it is unlikely that the person was subjected to labour exploitation"
    )
else:
    st.markdown(
        "#### Based on your selection, it is likely that the person was subjected to labour exploitation"
    )


st.markdown("#")
st.markdown("#")
st.markdown("#")
st.markdown("#")
st.markdown("#")
#ngrams (first img)

st.markdown("## N-grams for analysis")

st.image(
    "https://res.cloudinary.com/julioeq29/image/upload/v1638295006/img_2.png")

st.write("##")
st.write("##")
#ngrams (second img)


st.image(
    "https://res.cloudinary.com/julioeq29/image/upload/v1638295006/img_3.png")

st.write("##")
st.write("##")
#ngrams (third img)
st.markdown("## DistilBERT")

st.image(
    "https://res.cloudinary.com/julioeq29/image/upload/v1638295006/img_4.png")

st.write("##")
st.write("##")
#ngrams (fourth img)
st.image(
    "https://res.cloudinary.com/julioeq29/image/upload/v1638295007/img_5.png")

st.write("##")
st.markdown(
    """#### The data used in this website were obtained from more than 1,300 survivor testimonies published by the Nottingham Rights Lab, and from the CTDC dataset, which contains more than 90,000 records.
    """)
