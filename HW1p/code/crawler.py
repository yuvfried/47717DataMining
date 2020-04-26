from utils import get_page_response, make_soup
import pandas as pd


def get_egg_free_pages(url, stop_after_300=True):
    """
Crawls all the urls of egg-free recipes from the Allmain page of this section.
    @param url: string, url of the egg-free main page.
    @param stop_after_300: bool, indicates if only 300 pages are desired.
    @return: list, contains responses (type request.response) of the sub-pages
                of the main page
    """
    responses = []
    i = 1
    while True:
        # print(f'crawling page {i}')
        # We've note that the egg-free main page includes sub-pages,
        # which consist of the recipes.
        page = str(i)
        url += "?page=" + page
        r = get_page_response(url)
        if isinstance(r, Exception):
            print(f'exception was raised in page {page}')
            print(r)
            return None

        # examine why the request didn't work, it may be just the end of the egg-free content
        if r.status_code != 200:
            # print(f"loop breaks due page {page} doesn's have status code 200." + \
            #       f"\n{URL} has a status code: {r.status_code}")
            return responses

        responses.append(r)
        i += 1

        # 10 sub-pages are enough for crawling 300 recipes, so in order to reduce
        # requests and running time we'll stop here. It's easy to see the code
        # is available to crawl the whole egg-free section if we want to.
        # we'd just have to insert False to the arg stop_after_300.
        if i == 10 and stop_after_300:
            return responses


def crawl_urls(response):
    """
Crawls the urls for recipes from the main page sub-pages
    @param response: a request.response obj of one of the egg-free main page
                        sub-pages.
    @return: Pandas Series of links for recipes
    """
    soup = make_soup(response)
    urls = [link.get('href') for link in soup.find_all('a')]
    s = pd.Series(urls).dropna()
    # only links for recpies
    s = s[s.str.startswith("https://www.allrecipes.com/recipe/")]
    s = s.drop_duplicates()
    return s


# merge the pandas serieses to one long list of urls
def merge_urls(responses_lst):
    """
merges the urls from all Pandas serieses
    @param responses_lst: list contains all responses of the sub-pages
    @return: list with the whole desired recipes's urls
    """
    ser_lst = [crawl_urls(r) for r in responses_lst]
    return pd.concat(ser_lst).tolist()


def get_urls_lst(main_url):
    responses = get_egg_free_pages(main_url)
    return merge_urls(responses)
