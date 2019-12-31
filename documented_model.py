from __future__ import absolute_import

import time

from conf import (
    TRAIN_MODE,
    ARTIST_NAME,
    DEPTH_OF_THE_N_NETWORK,
    FILE_WITH_GENERATED_LYRICS,
)
from logger_conf import logger
from lyrics_generation import vectors_into_song, compose_rap, generate_lyrics
from neural_network import train, build_dataset, create_network
from utils import split_lyrics_file, prepare_list_of_all_rhymes


def main(depth, train_mode):
    start = time.time()
    model = create_network(depth, ARTIST_NAME=ARTIST_NAME, TRAIN_MODE=TRAIN_MODE)
    # change the lyrics file to the file with the lyrics you want to be trained on
    text_file = "ostr_lyrics.txt"

    if train_mode == True:
        bars = split_lyrics_file(text_file)

    if train_mode == False:
        bars = generate_lyrics(text_file)
        logger.debug("Generated lyrics:")
        logger.debug(bars)

    rhyme_list = prepare_list_of_all_rhymes(bars)
    if train_mode == True:
        x_data, y_data = build_dataset(bars, rhyme_list)
        train(x_data, y_data, model)

    if train_mode == False:
        vectors = compose_rap(bars, rhyme_list, text_file, model)
        rap = vectors_into_song(vectors, bars, rhyme_list)
        # f = open(FILE_WITH_GENERATED_LYRICS, "w")
        # for bar in rap:
        #     f.write(bar)
        #     f.write("\n")
        return rap
    stop = time.time()
    logger.info("Execution time in sec:{}".format(stop - start))


main(DEPTH_OF_THE_N_NETWORK, TRAIN_MODE)
