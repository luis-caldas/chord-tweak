# -*- coding: utf-8 -*-

"""
Functions to aid dynamic regex construction
"""

import re

from conf import config


def string_matrix_to_char_set(string_matrix, unwanted_chars):
    """
    :param string_maxtrix: [[str()]]
    """

    # create the set of chars in the chords
    chords_chars = set()

    # extract all the chars in the chords list
    # !gorgeous nesting
    for each_tone in string_matrix:
        for each_name in each_tone:
            for each_char in each_name:
                if each_char not in unwanted_chars:
                    chords_chars.add(each_char)

    # transform it to a tidy regex char set
    return "[%s]" % "".join(sorted(chords_chars))

def string_list_to_OR_group(string_list, name_id=None):
    return "(%s%s)" % (
        config.add_name_to_group(name_id) if name_id is not None else "",
        "".join(
            ["%s|" % re.escape(each_string) for each_string in sorted(string_list)[::-1]]
        )
    )

def create_full_chord_regex(start_chord_regex, chars_a, chars_b, quality_intervals_regex):
    # create the chord regex
    full_chord_regex = "%s%s%s%s" % (
        start_chord_regex,
        chars_a,
        quality_intervals_regex,
        chars_b
    )

    # return the full chord regex
    return full_chord_regex

def compile_regex():

    # get the cords char set
    chords_char_regex = "(%s%s+)" % (
        config.add_name_to_group(1),
        string_matrix_to_char_set(config.CHORDS_LIST, config.CHORDS_LIST_FREE_CHARS)
    )

    # create the free chars regex
    free_chars_regex_first = string_list_to_OR_group(config.CHORDS_LIST_FREE_CHARS, 2)
    free_chars_regex_second = string_list_to_OR_group(config.CHORDS_LIST_FREE_CHARS, 3)

    # build the quality and intervals regex
    quality_intervals_regex = "%s%s" % (
        string_list_to_OR_group(config.CHORD_QUALITY, 4),
        string_list_to_OR_group(config.CHORD_INTERVALS, 5)
    )

    # create the full regex
    full_regex = create_full_chord_regex(
        chords_char_regex,
        free_chars_regex_first,
        free_chars_regex_second,
        quality_intervals_regex
    )

    # return the full regex
    return full_regex

def line_regex(full_chord_regex):
    # create the regex of thing that may be in the chords line
    possible_chars_in_line = string_list_to_OR_group(config.REGEX_POSSIBLE_CHARS_CHORDS_LINE)

    # create the full needed regex
    return "^(( *)(%s)( *)(%s%s)( *)(%s)( *))+$" % (
        possible_chars_in_line,
        config.add_name_to_group(0),
        full_chord_regex,
        possible_chars_in_line
    )

def run_regex_on_single_line(line_regex_string, each_line):
    return re.match(line_regex_string, each_line)
