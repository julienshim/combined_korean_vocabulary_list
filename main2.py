# experimental 

import os
import time
from imports.funcs_regenerate import regenerate_2
from imports.funcs_loader import load_body
from imports.funcs_fragmentizers_sanitizers import go_fragmentize_sanitize, cheese_fragmentize_sanitize
from imports.funcs_write import generate_tsv
from imports.funcs_converters import line_arr_to_line_string
from imports.lists import combined_headers

start_time = time.time()

# load body from csv
go_body = load_body('./input/koreagokr/koreangokr.tsv')
cheese_body_1 = load_body('./input/cheeseonly.tsv')
cheese_body_2 = load_body('./input/cheese2only.tsv')
cheese_body = cheese_body_1 + cheese_body_2

go_fs_body = list(map(go_fragmentize_sanitize, go_body))
cheese_fs_body = list(map(cheese_fragmentize_sanitize, cheese_body))

# compare go and cheese and update english
regenerated_c_fs_body = regenerate_2(go_fs_body, cheese_fs_body)

# # create test.csv, create output folder in current working director if one does not exist
output_folder = 'output'
output_filename = 'test.tsv'
header_string = line_arr_to_line_string(combined_headers)

generate_tsv(header_string, regenerated_c_fs_body, output_folder, output_filename)

print("--- %s seconds ---" % (time.time() - start_time))