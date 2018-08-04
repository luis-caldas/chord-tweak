# -*- coding: utf-8 -*-

"""
The main config file for the chord tweaker

Can be changed at will considering base knowledge of the script
"""

# list of chords ordered by tones
# the nested list hosts equivalent chords
CHORDS_LIST = [
    ["C", "B#"],
    ["C#", "Db"],
    ["D"],
    ["D#", "Eb"],
    ["E", "Fb"],
    ["F", "E#"],
    ["F#", "Gb"],
    ["G"],
    ["G#", "Ab"],
    ["A"],
    ["A#", "Bb"],
    ["B", "Cb"]
]

CHORDS_LIST_FREE_CHARS = ["#", "b"]

# # addons to the chords

# the most used chord qualities
CHORD_QUALITY = [
    "m", "min", "-",
    "M", "maj", "+",
    "d", "dim", "°"
]

# the most used intervals
CHORD_INTERVALS = [
    "1", "2", "3", "4", "5", "6", "7", "9", "11", "13"
]

# #

# # regex utils

# regex group naming
USE_NAMING = True

# the group naming chosen to be used
REGEX_GROUP_NAMES = [
    "entire",  #  0 - the entire regex of a chord
    "sym",  #     1 - the cords symbol
    "semta",  #   2 - the first sharp group
    "semtb",  #   3 - the second sharp group
    "qual",  #    4 - the quality of the chord
    "int",  #     5 - the interval of the chord
]

# chars that may be in the chords line
REGEX_POSSIBLE_CHARS_CHORDS_LINE = [
    "/", "|", "*"
]

# function to help the naming convention
def add_name_to_group(name_id):
    return "?P<%s>" % REGEX_GROUP_NAMES[name_id % len(REGEX_GROUP_NAMES)] if bool(USE_NAMING) else ""

# #
