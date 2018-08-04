# -*- coding: utf-8 -*-

"""
Utility functions used by the tweaker
"""

import re

from conf import config

#############
# Variables #
#############

# coloring needed
COLOR = {
    "pop": '\033[41;1;33m',
    "end": '\033[0m'
}

#############

def print_true_lines(line_list, boolean_line_list):

    # iterate over the lines and print each
    for index_line, each_line in enumerate(line_list):

        # pop the colors of the true lines
        print("%s%s%s" % (
            COLOR["pop"] if boolean_line_list[index_line] else "",
            each_line,
            COLOR["end"] if boolean_line_list[index_line] else ""
        ), end="")

# list extrapolation helper with negative support
def list_runner(jump, list):

    # store the list length
    list_len = len(list)

    # is the jump to the left or right (negative or positive respectively)
    right = jump > 0

    # if to the right to the extrapolation jump
    if right:
        return list[jump % list_len]
    # if to the left too
    else:
        return list[-(abs(jump) % list_len)]

def replace_string_piece(start, end, string_input, string_insert):
    # removes a piece of string with its indexes and inserts a new one instead
    start_piece = string_input[:start]
    end_piece = string_input[end:]

    # return the new string
    return "%s%s%s" % (start_piece, string_insert, end_piece)

def tone_fix_chord(chord_regex_group_match, tone_upgrade):

    # get the group dict
    group_dict = chord_regex_group_match.groupdict()

    # variable assingment
    semitone = group_dict[config.REGEX_GROUP_NAMES[2]] or group_dict[config.REGEX_GROUP_NAMES[3]]
    chord = group_dict[config.REGEX_GROUP_NAMES[1]]

    # set the semitone assigment variable
    semitone_number = None

    # retrieve the chord semitone in number
    for index, each_semitone in enumerate(config.CHORDS_LIST):
        if "%s%s" % (chord, semitone) in each_semitone:
            semitone_number = index

    # some error checking (should never occur)
    if semitone_number is None:
        raise(ValueError("Found a retarded chord"))

    # update the tone number with the upgrade
    new_tone = semitone_number + tone_upgrade

    # get the new tone from the list with its number
    new_chord = list_runner(new_tone, config.CHORDS_LIST)[0]

    # rebuild the full chord
    full_new_chord = "%s%s%s" % (
        new_chord,
        group_dict[config.REGEX_GROUP_NAMES[4]],
        group_dict[config.REGEX_GROUP_NAMES[5]]
    )

    # return the new formed chord
    return full_new_chord

def tone_fix_line(tone_upgrade, chord_regex, line_string):

    # find every instance of the regex in the line string
    # found_regexes = [each_group[0] for each_group in re.findall("(%s)" % chord_regex, line_string)]
    found_regexes = [each for each in re.finditer("(%s)" % chord_regex, line_string)]

    # if not found there is an error
    if found_regexes is None:
        raise(ValueError("Regex did not find any chords in a falsely given string"))

    # create the replace nested list [[to_replace, replacement]]
    replace_list = list()

    # iterate over the found regexes and fix the chord with the new tone
    for each_found in found_regexes[::-1]:

        # get the new index
        new_chord = tone_fix_chord(each_found, tone_upgrade)

        # add the combo to the replacing list
        replace_list.append([each_found, new_chord])

    # replace the chords in the line
    for each_duo in replace_list:

        line_string = replace_string_piece(
            each_duo[0].start(),
            each_duo[0].end(),
            line_string,
            each_duo[1]
        )

    # return the replaced line
    return line_string
