import os

def load_body(address):
    with open(address) as tsv_file:
        tsv_file_headers = tsv_file.readline() # cuts the headers
        return tsv_file.readlines() # cuts the content
        tsv_file.close()
