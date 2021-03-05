from os import chdir, getcwd, path, makedirs
from imports.funcs_converters import line_arr_to_line_string


def generate_tsv(header_string, combined_arr, output_folder, output_filename):
    parent_dir = getcwd() # still in root folder
    sub_path = path.join(parent_dir, output_folder)
    if not path.exists(sub_path):
        makedirs(sub_path)
    with open(path.join(sub_path, output_filename), 'w') as tsv_file:
        # write header
        tsv_file.writelines(header_string)
        # write content
        for line_arr in combined_arr:
            line_string = line_arr_to_line_string(line_arr)
            tsv_file.writelines(line_string)
        tsv_file.close()
