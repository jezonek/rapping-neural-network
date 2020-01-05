from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import Session, ConnectionError

from logger_conf import logger

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
    collection = prepare_connection_to_db_rhymes()
    logger.debug("Looking in db for {}".format(word))
    check = word_is_in_db(word, collection)
    if check:
        logger.debug("Found {}".format(check))
        return check["rhymes"]
    logger.debug("Looking remote")
    result = find_rhyme_on_remote(word)
    record = {"word": word,
              "rhymes": result}
    logger.debug("Putting into db: {}".format(record["word"]))
    collection.insert_one(record)
    return result


def prepare_connection_to_db_rhymes():
    client = MongoClient("mongo:27017", username="root", password="example")
    db = client.rhymes_db
    collection = db.rhymes
    return collection

def prepare_connection_to_db_texts():
    client = MongoClient("mongo:27017", username="root", password="example")
    db = client.rhymes_db
    collection = db.done_texts
    return collection


def word_is_in_db(word, collection):
    return collection.find_one({"word": word})
