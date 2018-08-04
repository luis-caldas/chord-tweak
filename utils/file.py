# -*- coding: utf-8 -*-

"""
Self made functions for file manupulation
"""

def file_to_line_list(file_name):

    with open(file_name, 'r') as file_pointer:
        return list(file_pointer)
