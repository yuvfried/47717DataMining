import requests
from bs4 import BeautifulSoup
from time import sleep


def get_page_response(url, delay=1):
    try:
        response = requests.get(url)
    except Exception as e:
        return e
    sleep(delay)
    return response


def make_soup(response):
    return BeautifulSoup(response.text, features='lxml')


