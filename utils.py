import os
import re

import markovify

from conf import MAXIMUM_SYLLABLES_PER_LINE, TRAIN_MODE, ARTIST_NAME
from logger_conf import logger
from rhyme_finding import find_rhyme


def create_markov_model(text_file):
    read = open(text_file, "r").read()
    # markovify goes line by line of the lyrics.txt file and
    # creates a model of the text which allows us to use
    # make_sentence() later on to create a bar for lyrics
    # creates a probability distribution for all the words
    # so it can generate words based on the current word we're on
    text_model = markovify.NewlineText(read)
    return text_model


def split_lyrics_file(text_file):
    text = open(text_file).read()
    text = text.split("\n")
    while "" in text:
        text.remove("")
    return text


def convert_index_of_most_common_rhyme_into_float(line, rhyme_list):
    word = re.sub(r"\W+", "", line.split(" ")[-1]).lower()

    rhymeslist = find_rhyme(word)
    logger.debug("Looking for rhyme for: {}".format(word))
    rhymeslistends = []
    for i in rhymeslist:
        rhymeslistends.append(i[-2:])
    try:
        ordered_rhyme_ends = max(set(rhymeslistends), key=rhymeslistends.count)

        ordered_rhyme_ends = ordered_rhyme_ends.decode("utf-8")
    except AttributeError:
        ordered_rhyme_ends = ordered_rhyme_ends
    except Exception:
        ordered_rhyme_ends = word[-2:]
    try:
        float_rhyme = rhyme_list.index(ordered_rhyme_ends)
        float_rhyme = float_rhyme / float(len(rhyme_list))
        logger.info("Calculated floatrhyme: {}".format(float_rhyme))
        return float_rhyme
    except ValueError as e:
        logger.error("Value Error: {}".format(e.__str__()))
        return 0


def load_saved_rhymes_file(ARTIST_NAME):
    logger.debug("loading saved rhymes from " + str(ARTIST_NAME) + ".rhymes")
    return open(str(ARTIST_NAME) + ".rhymes", "r").read().split("\n")


def calculate_count_of_syllables_as_fraction(line):
    count = 0
    for word in line.split(" "):
        vowels = "aeiouy"
        word = word.lower().strip(".:;?!")
        try:
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index - 1] not in vowels:
                    count += 1
            if word.endswith("e"):
                count -= 1
            if word.endswith("le"):
                count += 1
            if count == 0:
                count += 1
        except IndexError:
            logger.error("Error occured during syllables: {}".format(word))
            continue
        return count / MAXIMUM_SYLLABLES_PER_LINE


def prepare_list_of_all_rhymes(lyrics):
    if TRAIN_MODE == False:
        return load_saved_rhymes_file(ARTIST_NAME)
    elif TRAIN_MODE == True and os.path.isfile("{}.rhymes".format(ARTIST_NAME)):
        with open("{}.rhymes".format(ARTIST_NAME), "r") as opened_file:
            return opened_file.read().splitlines()
    else:
        return build_new_rhyme_list(lyrics)


def build_new_rhyme_list(lyrics):
    rhyme_master_list = []
    logger.debug("Alright, building the list of all the rhymes")
    for i in lyrics:
        # grabs the last word in each bar
        word = re.sub(r"\W+", "", i.split(" ")[-1]).lower()
        # fixed scrapy spider for searching rhymes in web

        rhymeslist = find_rhyme(word)
        # need to convert the unicode rhyme words to UTF8
        logger.debug(rhymeslist)
        # rhymeslistends contains the last two characters for each word
        # that could potentially rhyme with our word
        rhymeslistends = []
        for i in rhymeslist:
            rhymeslistends.append(str(i[-2:]))
        try:
            # rhymescheme gets all the unique two letter endings and then
            # finds the one that occurs the most
            rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
        except Exception:
            rhymescheme = word[-2:]
        rhyme_master_list.append(rhymescheme)
    # rhyme_master_list is a list of the two letters endings that appear
    # the most in the rhyme list for the word
    rhyme_master_list = list(set(rhyme_master_list))
    reverselist = [x[::-1] for x in rhyme_master_list]
    reverselist = sorted(reverselist)
    # rhymelist is a list of the two letter endings (reversed)
    # the reason the letters are reversed and sorted is so
    # if the network messes up a little bit and doesn't return quite
    # the right values, it can often lead to picking the rhyme ending next to the
    # expected one in the list. But now the endings will be sorted and close together
    # so if the network messes up, that's alright and as long as it's just close to the
    # correct rhymes
    rhymelist = [x[::-1] for x in reverselist]
    f = open(str(ARTIST_NAME) + ".rhymes", "w")
    f.write("\n".join(rhymelist))
    f.close()
    logger.debug(rhymelist)
    return rhymelist
