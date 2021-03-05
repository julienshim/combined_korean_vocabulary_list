import os
import time
from re import sub
from imports.funcs_regenerate import regenerate
from imports.funcs_loader import load_body
from imports.funcs_fragmentizers_sanitizers import go_fragmentize_sanitize, topik_fragmentize_sanitize
from imports.funcs_write import generate_tsv
from imports.funcs_converters import line_arr_to_line_string
from imports.funcs_shift_values import shift_values
from imports.funcs_remove_duplicates import remove_duplciates
from imports.lists import combined_headers

start_time = time.time()

# load body from csv
go_body = load_body('./input/koreagokr/koreangokr.tsv')
topik_body = load_body('./input/topik/topik.tsv')

# rearrange go and topik content under the following headers:
# 0. frequency 1. korean 2. pos 3. hanja 4. hanja 5. hint 6. go 7. topik
go_fs_body = list(map(go_fragmentize_sanitize, go_body))
topik_fs_body = list(map(topik_fragmentize_sanitize, topik_body))

# sort combined go and topik content by korean (not accounting dashes) and part of speech
combined_fs_body = sorted(go_fs_body + topik_fs_body, key=lambda line: (sub('-','',line[1]), line[2]))

# compare cells and reformat hint column
regenerated_c_fs_body = regenerate(combined_fs_body)

# allow lines with frequencies to inheret values from non frequency lines
shifted_r_c_fs_body = shift_values(regenerated_c_fs_body)

# remove duplicates
unique_s_r_c_fs_body = remove_duplciates(shifted_r_c_fs_body)

# create test.csv, create output folder in current working director if one does not exist
output_folder = 'output'
output_filename = 'combined_topik_go.tsv'
header_string = line_arr_to_line_string(combined_headers)

generate_tsv(header_string, unique_s_r_c_fs_body, output_folder, output_filename)

print("--- %s seconds ---" % (time.time() - start_time))