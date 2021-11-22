from bs4 import BeautifulSoup
import requests
import re
import csv

def take_url():
    lista_finale_url = list()
    for i in range(1, 69):
        response = requests.get(
            "http://antislavery.ac.uk/solr-search?facet=collection%3A%22VOICES%3A+Narratives+by+Survivors+of+Modern+Slavery%22&page={number}"
            .format(number=i))
        html = response.text
        soup = BeautifulSoup(html,features="html.parser")
        img = soup.find_all("a")
        lista = [i.get("href") for i in img]
        for i in lista:
            if type(i) == str:
                if re.findall(".*items.*", i):
                    lista_finale_url.append(i)

    final_list = ["http://antislavery.ac.uk" + i for i in lista_finale_url]
    return final_list

list_url=take_url()
print(len(list_url))
