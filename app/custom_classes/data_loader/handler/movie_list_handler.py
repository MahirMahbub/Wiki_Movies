from typing import Any
from typing import Any
from typing import List, Dict

import pandas as pd
import requests as requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from pandas import DataFrame
from requests import request

from app.custom_classes.data_loader.handler.abstract_handler import AbstractHandler


class MovieListHandler(AbstractHandler):
    def execute(self, request_data: str) -> List[Dict[Any, Any]]:
        request_handler: request = requests.get(request_data)
        html_table: Tag = BeautifulSoup(features="lxml", markup=request_handler.text).find('table')
        request_handler.close()

        wiki_films_df: DataFrame = pd.read_html(str(html_table), header=0)[0]
        links: List[str] = []
        for tr in html_table.findAll("tr"):
            trs: ResultSet = tr.findAll("td")
            for td in trs:
                try:
                    if td.i:
                        movie_wiki_link: str = r"https://en.wikipedia.org/" + td.i.find('a')["href"]
                        links.append(movie_wiki_link)
                except TypeError as type_e:
                    links.append("")
                    pass
                except AttributeError as attr_e:
                    links.append("")
                    pass

        wiki_films_df['Wiki Link'] = links
        wiki_films_df["id"] = [i for i in range(1, len(links) + 1)]
        return wiki_films_df.to_dict(orient='records')

    def handle(self, request_data: Any):
        return super().handle(request_data)
