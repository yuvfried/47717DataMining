import re
import json


def init_record_recipe(url):
    return {"url":url, "id":get_id(url)}


# gets key, url, source exception info
def exception_message(key,url,exception_obj):
    message = f"An error occurred when crawling recipe key: {key}\n" +\
              f"Recipre's URL: {url}" +\
              f"This is the original exception error:\n{exception_obj}"
    print(message)


def get_id(url):
    return re.search("\d+[^/]",url).group()


def get_title(d, soup):
    try:
        title = soup.find('h1').text
    except Exception as e:
        exception_message("title", d['url'], e)
        title = None

    d["title"] = title


def get_rating(d, soup):
    try:
        rating = soup.find_all('meta', attrs={"name": "og:rating"})[0]['content']
    except Exception as e1:
        try:
            lst = soup.find_all(attrs={'class': 'recipe-summary__stars'})
            nested_lst = [i.find_all(attrs={'data-ratingstars': True}) for i in lst]
            rating = nested_lst[0][0]['data-ratingstars']
        except Exception as e2:
            exception_message("rating", d['url'], e1)
            exception_message("rating", d['url'], e2)
            rating = None
    d['rating'] = rating


# returns array of strings
def get_ingredients(d,soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        ingredients = json_script[1]['recipeIngredient']
    except Exception as e1:
        try:
            ingredients = [i.text for i in soup('span', {'itemprop': "recipeIngredient"})]
        except Exception as e2:
            exception_message("ingredients",d['url'],e1)
            exception_message("ingredients", d['url'], e2)
            ingredients = None

    d['ingredients'] = ingredients


# returns an array of strings(d, soup)
def get_directions(d, soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        directions = [d['text'] for d in json_script[1]['recipeInstructions']]
    except Exception as e1:
        try:
            inst_lst = []
            for i in soup('span', {'class': "recipe-directions__list--item"}):
                inst = i.text
                if not re.search('[A-z]', inst):
                    continue
                inst = re.sub('\s+', ' ', inst)
                inst = re.sub(" $", '', inst)
                inst_lst.append(inst)
            directions = inst_lst
        except Exception as e2:
            exception_message("directions",d['url'],e1)
            exception_message("directions", d['url'], e2)
            directions = None

    d['directions'] =directions


def get_creator(d, soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        creator = json_script[1]['author']['name']
    except Exception as e1:
        try:
            creator = soup.find_all('span', attrs={'itemprop': 'author'})[0].text
        except Exception as e2:
            exception_message("creator",d['url'],e1)
            exception_message("creator", d['url'], e2)
            creator = None

    d['creator'] = creator


def get_preptime(d, soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        preptime =json_script[1]['prepTime']
    except Exception as e1:
        try:
            preptime = soup('time',attrs={'itemprop':'prepTime'})[0]['datetime']
        except Exception as e2:
            exception_message("PrepTime",d['url'],e1)
            exception_message("PrepTime", d['url'], e2)
            preptime = None

    d['PrepTime'] = preptime


def get_cooktime(d, soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        cooktime =json_script[1]['cookTime']
    except Exception as e1:
        try:
            cooktime = soup('time',attrs={'itemprop':'cookTime'})[0]['datetime']
        except Exception as e2:
            exception_message("CookTime",d['url'],e1)
            exception_message("CookTime", d['url'], e2)
            cooktime = None

    d['CookTime'] = cooktime


def get_totaltime(d, soup):
    try:
        script = soup('script', attrs={"type": "application/ld+json"})[0].find(text=True).strip()
        json_script = json.loads(script)
        totaltime =json_script[1]['totalTime']
    except Exception as e1:
        try:
            totaltime = soup('time',attrs={'itemprop':'totalTime'})[0]['datetime']
        except Exception as e2:
            exception_message("TotalTime",d['url'],e1)
            exception_message("TotalTime", d['url'], e2)
            totaltime = None

    d['TotalTime'] = totaltime


def get_num_reviews(d, soup):
    try:
        reviews_str = soup('a', attrs={'class': "ugc-ratings-link ugc-reviews-link"})[0].text
        num_rev = re.findall('\d+', reviews_str, flags=re.DOTALL)[0]
    except Exception as e1:
        try:
            reviews_str = soup('span', attrs={'class': 'review-count'})[0].text
            num_rev = re.findall('\d+', reviews_str, flags=re.DOTALL)[0]
        except Exception as e2:
            exception_message("NumReviews",d['url'],e1)
            exception_message("NumReviews", d['url'], e2)
            num_rev = None

    d['NumReviews'] = num_rev


def get_servings(d, soup):
    try:
        servs_str = soup('div', attrs={'class': "recipe-adjust-servings__original-serving"})[0].text
        num_serv = re.findall('\d+', servs_str, flags=re.DOTALL)[0]
    except Exception as e1:
        try:
            num_serv = soup('meta', attrs={'itemprop': "recipeYield"})[0]['content']
        except Exception as e2:
            exception_message("Servings", d['url'], e1)
            exception_message("Servings", d['url'], e2)
            num_serv = None

    d["Servings"] = num_serv


# applying all the above functions
def record_recipe(url, soup):
    d = init_record_recipe(url)
    get_id(url)
    get_title(d, soup)
    get_creator(d, soup)
    get_rating(d, soup)
    get_num_reviews(d, soup)
    get_ingredients(d, soup)
    get_directions(d, soup)
    get_preptime(d, soup)
    get_cooktime(d, soup)
    get_totaltime(d, soup)
    get_servings(d, soup)
    return d


