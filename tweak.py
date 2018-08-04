#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from copy import deepcopy

from conf import config
from utils import file as local_file
from utils import regex as local_regex
from utils import utils as local_utils


def main():

    # create the argument parser
    parser = argparse.ArgumentParser(description="Tweak tones in music files with chords, remember that 1 octave is 12 semitones")

    # add the needed arguments
    parser.add_argument("filename", type=str, help="The file that contains the chords")
    parser.add_argument("--step", default=0, type=int, help="The semitone step for the chords like +1, -3, +3")
    parser.add_argument("--check", action="store_true", help="Print the lines that will be updated and exit")
    parser.add_argument("--regex", action="store_true", help="Print a header containing the regex used by the source")

    # parse the args
    args = parser.parse_args()

    # get the file given
    line_list = local_file.file_to_line_list(args.filename)

    # create the needed regexes
    chord_regex_string = local_regex.compile_regex()
    line_regex_string = local_regex.line_regex(chord_regex_string)

    # print the regexes
    if args.regex:
        print("Chord regex:", chord_regex_string)
        print("Full line regex:", line_regex_string)
        print("")

    # list that will store boolean for the lines that have chords
    boolean_line_list = list()

    # get the lines in the file that are chords lines
    for each_line in line_list:

        # check with the regex for chords
        found_regex = local_regex.run_regex_on_single_line(line_regex_string, each_line)

        # add to the equivalent boolean list the truth about containing chords
        boolean_line_list.append(bool(found_regex is not None))

    # if asked to show lines show 'em
    if args.check:
        local_utils.print_true_lines(line_list, boolean_line_list)
        return

    # create the new file line list
    new_line_list = deepcopy(line_list)

    # tone fix all the true lines
    for index, each_line in enumerate(line_list):
        if boolean_line_list[index]:
            new_line_list[index] = local_utils.tone_fix_line(args.step, chord_regex_string, each_line)

    # print each new line for the user
    for index, each_line in enumerate(new_line_list):
        print(each_line, end="")

if __name__ == "__main__":
    main()
