import random

import numpy as np

from conf import MAXIMUM_SYLLABLES_PER_LINE
from utils import (
    create_markov_model,
    split_lyrics_file,
    convert_index_of_most_common_rhyme_into_float,
    calculate_count_of_syllables_as_fraction,
)


def vectors_into_song(vectors, generated_lyrics, rhyme_list):
    print("\n\n")
    print("About to write rap (this could take a moment)...")
    print("\n\n")

    # compare the last words to see if they are the same, if they are
    # increment a penalty variable which grants penalty points for being
    # uncreative
    def last_word_compare(rap, line2):
        penalty = 0
        for line1 in rap:
            try:
                word1 = line1.split(" ")[-1]
                word2 = line2.split(" ")[-1]

                # remove any punctuation from the words
                while word1[-1] in "?!,. ":
                    word1 = word1[:-1]

                while word2[-1] in "?!,. ":
                    word2 = word2[:-1]

                if word1 == word2:
                    penalty += 0.2
            except IndexError:
                print("Error in last word compare :{}".format(line2))
                continue

        return penalty

    # vector_half is a single [syllable, rhyme_index] pair
    # returns a score rating for a given line
    def calculate_score(vector_half, syllables, rhyme, penalty):
        desired_syllables = vector_half[0]
        desired_rhyme = vector_half[1]
        # desired_syllables is the number of syllables we want
        desired_syllables = desired_syllables * MAXIMUM_SYLLABLES_PER_LINE
        # desired rhyme is the index of the rhyme we want
        desired_rhyme = desired_rhyme * len(rhyme_list)

        # generate a score by subtracting from 1 the sum of the difference between
        # predicted syllables and generated syllables and the difference between
        # the predicted rhyme and generated rhyme and then subtract the penalty
        try:
            score = (
                1.0
                - (
                    abs((float(desired_syllables) - float(syllables)))
                    + abs((float(desired_rhyme) - float(rhyme)))
                )
                - penalty
            )
            print(
                "Calculed_score({},{},{},{})".format(
                    vector_half, syllables, rhyme, penalty
                )
            )
            return score
        except TypeError:
            print(
                "Error occured durind calculed_score({},{},{},{})".format(
                    vector_half, syllables, rhyme, penalty
                )
            )
            return None

    # generated a list of all the lines from generated_lyrics with their
    # line, syllables, and rhyme float value
    dataset = []
    for line in generated_lyrics:
        line_list = [
            line,
            calculate_count_of_syllables_as_fraction(line),
            convert_index_of_most_common_rhyme_into_float(line, rhyme_list),
        ]
        dataset.append(line_list)

    rap = []

    vector_halves = []
    for vector in vectors:
        # vectors are the 2x2 rap_vectors (predicted bars) generated by compose_rap()
        # separate every vector into a half (essentially one bar) where each
        # has a pair of [syllables, rhyme_index]
        vector_halves.append(list(vector[0][0]))
        vector_halves.append(list(vector[0][1]))

    for vector in vector_halves:
        # Each vector (predicted bars) is scored against every generated bar ('item' below)
        # to find the generated bar that best matches (highest score) the vector predicted
        # by the model. This bar is then added to the final rap and also removed from the
        # generated lyrics (dataset) so that we don't get duplicate lines in the final rap.
        scorelist = []
        for item in dataset:
            # item is one of the generated bars from the Markov model
            line = item[0]

            if len(rap) != 0:
                penalty = last_word_compare(rap, line)
            else:
                penalty = 0
            # calculate the score of the current line
            total_score = calculate_score(vector, item[1], item[2], penalty)
            score_entry = [line, total_score]
            # add the score of the current line to a scorelist
            scorelist.append(score_entry)

        fixed_score_list = []
        for score in scorelist:
            try:
                fixed_score_list.append(float(score[1]))
            except TypeError:
                continue
        # get the line with the max valued score from the fixed_score_list
        max_score = max(fixed_score_list)
        for item in scorelist:
            if item[1] == max_score:
                # append item[0] (the line) to the rap
                rap.append(item[0])
                print(str(item[0]))

                # remove the line we added to the rap so
                # it doesn't get chosen again
                for i in dataset:
                    if item[0] == i[0]:
                        dataset.remove(i)
                        break
                break
    return rap


def compose_rap(lines, rhyme_list, lyrics_file, model):
    rap_vectors = []
    human_lyrics = split_lyrics_file(lyrics_file)

    # choose a random line to start in from given lyrics
    initial_index = random.choice(range(len(human_lyrics) - 1))
    # create an initial_lines list consisting of 2 lines
    initial_lines = human_lyrics[initial_index : initial_index + 8]

    starting_input = []
    for line in initial_lines:
        # appends a [syllable, rhyme_index] pair to starting_input
        starting_input.append(
            [
                calculate_count_of_syllables_as_fraction(line),
                convert_index_of_most_common_rhyme_into_float(line, rhyme_list),
            ]
        )

    # predict generates output predictions for the given samples
    # it's reshaped as a (1, 2, 2) so that the model can predict each
    # 2x2 matrix of [syllable, rhyme_index] pairs
    starting_vectors = model.predict(
        np.array([starting_input]).flatten().reshape(4, 2, 2)
    )
    rap_vectors.append(starting_vectors)

    for i in range(49):
        rap_vectors.append(
            model.predict(np.array([rap_vectors[-1]]).flatten().reshape(4, 2, 2))
        )

    return rap_vectors


def generate_lyrics(lyrics_file):
    bars = []
    last_words = []
    lyriclength = len(open(lyrics_file).read().split("\n"))
    count = 0
    markov_model = create_markov_model(lyrics_file)

    while len(bars) < lyriclength / 9 and count < lyriclength * 2:
        # By default, the make_sentence method tries, a maximum of 10 times per invocation,
        # to make a sentence that doesn't overlap too much with the original text.
        # If it is successful, the method returns the sentence as a string.
        # If not, it returns None. (https://github.com/jsvine/markovify)
        bar = markov_model.make_sentence()

        # make sure the bar isn't 'None' and that the amount of
        # syllables is under the max syllables
        if (
            type(bar) != type(None)
            and calculate_count_of_syllables_as_fraction(bar) < 1
        ):

            # function to get the last word of the bar
            def get_last_word(bar):
                last_word = bar.split(" ")[-1]
                # if the last word is punctuation, get the word before it
                if last_word[-1] in "!.?,":
                    last_word = last_word[:-1]
                return last_word

            last_word = get_last_word(bar)
            # only use the bar if it is unique and the last_word
            # has only been seen less than 3 times
            if bar not in bars and last_words.count(last_word) < 3:
                bars.append(bar)
                last_words.append(last_word)
                count += 1

    return bars
