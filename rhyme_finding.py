import subprocess
import json
import os
import time


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


