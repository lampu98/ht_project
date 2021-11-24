from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import time
import csv

path = "raw_data/index_url.csv"
df=pd.read_csv(path)


def scrape():
    df_country = pd.read_csv(
        "/Users/fenice/code/QZKZ3/ht_project/raw_data/countries of the world.csv"
    )["Country"]
    country=list(df_country)
    country.append("North Korea")
    country.append("Sri Lank")
    country.append("Sri Lanka")

    themes = [
        "Sexual exploitation", "Children", "Forced labour", "Domestic slavery",
        "Forced marriage", "Trafficking", "Debt bondage", "War slavery",
        "Armed conflict", "Women", "Prison labour", "Migration", "Emancipation"
    ]

    with open('/Users/fenice/code/QZKZ3/ht_project/try.csv',
            'a',
            encoding='UTF8',
            newline='') as f:
        for i in [28,  36, 125, 526, 527, 528, 530, 902, 912, 913, 914, 915, 917,918, 919, 920, 921, 973]:

            print(i)
            link = df.loc[i].url
            response = requests.get(link)
            html = response.text
            soup = BeautifulSoup(html, features="html.parser")

            text = []
            for element in soup.find_all("div", class_="text-item-body no-select"):
                text.append(element.text.strip())
            final_text=' '.join(text).replace("\xa0"," ")

            try:
                for item in soup.find_all("div", class_= "item-title"):
                    name = item.find("h3", class_="item-title__title").text.split()[0]
                    narrative_year = item.find("h5", class_="item-title__meta").text.split()[0]
            except:
                name=np.nan
                narrative_year=np.nan

            inline_item = soup.find_all("li", {"class": "inline-meta__item"})

            all_items=[i.text.strip() for i in inline_item]

            countries=list()
            for i in all_items:
                for x in country:
                    if re.findall(x,i):
                        countries.append(x)
            len_countries=len(countries)

            if len_countries == 0:
                arrival= np.nan
                departure = np.nan
            elif len_countries == 1:
                arrival= countries[0]
            elif len_countries == 2:
                arrival = countries[0]
                departure = countries[1]
            elif len_countries == 3:
                arrival = [countries[0],countries[1]]
                departure = countries[2]
            elif len_countries == 4:
                arrival = [countries[0], countries[1], countries[2]]
                departure = countries[3]
            else:
                arrival = "Too much countries"
                departure = "Too much countries"

            themes_final = list()
            for i in all_items:
                for x in themes:
                    if re.findall(x, i):
                        themes_final.append(x)
            sum_themes = len(themes_final)


            if sum_themes == 0:
                theme= np.nan
            elif sum_themes == 1:
                theme= themes_final[0]
            elif sum_themes == 2:
                theme = [themes_final[0],themes_final[1]]
            else:
                theme="too much themes"

            try:
                maplocation = re.findall("mapLocation = .(.*).,",
                                        soup.find("script").text)[0]
                latitude = float(re.findall("(.*),", maplocation)[0])
                longitude = float(re.findall(",(.*)", maplocation)[0])
            except:
                latitude=np.nan
                longitude=np.nan

            try:
                date_slavery = re.findall("\d{4}-\d*", str(soup.find("section", class_="item-meta")))[0]
            except:
                date_slavery=np.nan

            dictionary = {
                "text": final_text,
                "name": name,
                "year": narrative_year,
                "departure": departure,
                "arrival": arrival,
                "theme": theme,
                "latitude": latitude,
                "longitude": longitude,
                "date_slavery": date_slavery
            }

            fieldnames= [
                "text","name",
                "year", "departure", "arrival", "theme", "latitude", "longitude",
                "date_slavery"
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(dictionary)

scrape()
