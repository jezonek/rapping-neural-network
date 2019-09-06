import subprocess
import json
import os
import time

from requests import get,post, Session
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


# from rymy.rymy.spiders.rymek import QuotesSpider
# from scrapy.crawler import CrawlerProcess


def run_rhyme_spider(word):
    if os.path.exists("rymy/rymy/rymy.json".format(word)):
        os.remove("rymy/rymy/rymy.json".format(word))

    subprocess.check_call(["scrapy", "crawl", "rymek", "-o", "rymy.json", "-a" "word={}".format(word)], cwd="rymy/rymy",
                          shell=False)
    # process= CrawlerProcess({'FEED_FORMAT': 'json'})
    # process.crawl(QuotesSpider, word=word)
    # process.start(stop_after_crawl=True)


def convert_json_to_list():

    with open("rymy/rymy/rymy.json", "r") as opened_file:
        content = opened_file.read()
        try:
            content=json.loads(content)
        except ValueError:
            return []
        return [element["rhyme"] for element in content]


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



def find_rhyme(word):
    s = Session()
    response = s.get("https://www.rymer.org/4.0.1/")
    html = BeautifulSoup(response.text, 'html.parser')
    selected = html.find(attrs={"name": "form_key"})
    key=selected["value"]
    data = {"wpisz_slowo":word,
            "LNG":"pl",
            "form_key":key,
            "slownik":"P",
            "minsyl":1,
            "maxsyl":5,
            "czemow":"A",
            "ileLIT":"slowo",
            "zjakichliter":"ALL",
            "mozliweLIT":""}
    r=s.post("https://www.rymer.org/4.0.1/search1.php",data=data)
    print(r.text)
