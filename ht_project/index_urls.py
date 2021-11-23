from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd

def take_url():
    all_url_list = list()
    for i in range(1, 69):
        response = requests.get(
            "http://antislavery.ac.uk/solr-search?facet=collection%3A%22VOICES%3A+Narratives+by+Survivors+of+Modern+Slavery%22&page={number}"
            .format(number=i))

        # I take the html response
        html = response.text
        soup = BeautifulSoup(html,features="html.parser")
        a = soup.find_all("a")

        #I get all the url inside my list a
        lista = [i.get("href") for i in a]
        for i in lista:
            if type(i) == str:
                if re.findall(".*items.*", i):
                    all_url_list.append(i)

    # I add at the beginning of every url inside all_url_list this path: http://antislavery.ac.uk
    final_list = ["http://antislavery.ac.uk" + i for i in all_url_list]
    return final_list

list_url=take_url()

#creating a DataFrame with the url list
df = pd.DataFrame(list_url)
