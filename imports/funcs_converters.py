
from re import sub

def strip(string):
    return string.strip()

def line_string_to_line_array(line_string):
    arr = sub('\n','',line_string).split('\t')
    arr_stripped = map(strip, arr)
    return arr_stripped

def line_arr_to_line_string(line_arr):
    arr_stripped = map(strip, line_arr)
    line_string = '\t'.join(arr_stripped)
    return f'{line_string}\n'