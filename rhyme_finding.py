import json
import os
import subprocess

from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import Session, ConnectionError

from logger_conf import logger


def run_rhyme_spider(word):
    if os.path.exists("rymy/rymy/rymy.json".format(word)):
        os.remove("rymy/rymy/rymy.json".format(word))

    subprocess.check_call(
        ["scrapy", "crawl", "rymek", "-o", "rymy.json", "-a" "word={}".format(word)],
        cwd="rymy/rymy",
        shell=False,
    )


def convert_json_to_list():
    with open("rymy/rymy/rymy.json", "r") as opened_file:
        content = opened_file.read()
        try:
            content = json.loads(content)
        except ValueError as e:
            logger.exception(e)
            return []
        return [element["rhyme"] for element in content]


def find_rhyme_on_remote(word):
    s = Session()
    try:
        response = s.get("https://www.rymer.org/4.0.1/")
        html = BeautifulSoup(response.text, "html.parser")
        selected = html.find(attrs={"name": "form_key"})
        key = selected["value"]
        data = {
            "wpisz_slowo": word,
            "LNG": "pl",
            "form_key": key,
            "slownik": "P",
            "minsyl": 1,
            "maxsyl": 5,
            "czemow": "A",
            "ileLIT": "slowo",
            "zjakichliter": "ALL",
            "mozliweLIT": "",
        }
        r = s.post("https://www.rymer.org/4.0.1/search1.php", data=data)
        rymy = BeautifulSoup(r.text, "html.parser")
        _2syl = rymy.findAll("div", class_=["syl2", "syl3", "syl4", "syl5"])
        rymy_final = []
        for row in _2syl:
            rymy_final = rymy_final + row.text.lstrip("2345-syl.:").split(", ")
        return rymy_final
    except ConnectionError as e:
        logger.exception(e)
        return []


def find_rhyme(word):
    collection = prepare_connection_to_db()
    logger.debug("Looking in db for {}".format(word))
    check = word_is_in_db(word, collection)
    if check:
        logger.debug("Found {}".format(check))
        return check["rhymes"]
    logger.debug("Looking remote")
    result = find_rhyme_on_remote(word)
    record = {"word": word,
              "rhymes": result}
    logger.debug("Putting into db: {}".format(record))
    collection.insert_one(record)
    return result


def prepare_connection_to_db():
    client = MongoClient("mongo:27017", username="root", password="example")
    db = client.rhymes_db
    collection = db.rhymes
    return collection


def word_is_in_db(word, collection):
    return collection.find_one({"word": word})
