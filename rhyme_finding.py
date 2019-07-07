import subprocess
import json
import os

def run_rhyme_spider(word):
    if os.path.exists("rymy/rymy/rymy.json"):
        os.remove("rymy/rymy/rymy.json")

    subprocess.call(["cd rymy/rymy","scrapy crawl rymek -o rymy.json -a word={}".format(word)], shell=True)

def convert_json_to_list():

    with open("rymy/rymy/rymy.json","w+") as opened_file:
        content=opened_file.read()
        return [element["rhyme"] for element in content]
