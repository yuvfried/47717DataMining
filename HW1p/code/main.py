from get_fields import record_recipe
from crawler import get_urls_lst
from utils import get_page_response, make_soup
import json


# return dict<->record
def record(url):
    """
    @param url: string of a recipe for crawling
    @return: a dict contains the desired fields name with their value
    """
    r = get_page_response(url, delay=1)
    soup = make_soup(r)
    return record_recipe(url, soup)


def make_out_d(urls):
    """
    @param urls: list of recipes to crawl from.
    @return: a dict represents the desired json object.
    """
    recipes_lst = []
    for url in enumerate(urls):
        recipes_lst.append(record(url))
    inner_d = {"record":recipes_lst}
    outer_d = {"records":inner_d}
    return outer_d


def save_out_as_json(out_d, filename):
    with open(filename, 'w') as json_file:
        json.dump(out_d, json_file, indent=4)


if __name__ == "__main__":
    EGG_FREE_URL = "https://www.allrecipes.com/recipes/740/healthy-recipes/egg-free/"
    urls = get_urls_lst(EGG_FREE_URL)
    out_d = make_out_d(urls)
    save_out_as_json(out_d, r'C:\Users\yuvalf\OneDrive\courses\term6\47717DataMining\HW1p\output\data.json')
