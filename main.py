import collections
import csv
import json
import os
import re
import time

import managers.data_manager as data_manager
import managers.merge_manager as merge_manager

start_time = time.time()


# Date Managers
nikl_data_manager = data_manager.DataManager()
nikl_data_manager.load_from_tsv_file(file_path="./data/raw/한국어 학습용 어휘 목록.tsv")
nikl_data = nikl_data_manager.get_entries()


topik_data_manager = data_manager.DataManager()
topik_data_manager.load_from_tsv_dir(directory="./data/raw/토픽 어휘 목록_공개 목록")
topik_data = topik_data_manager.get_entries()

# Merge Manager
vocabulary_manager = merge_manager.MergeManager()
vocabulary_manager.load_entries(entries=nikl_data)
vocabulary_manager.load_entries(entries=topik_data)
vocabulary_manager.sort_entries_by_keys(sorting_keys=["word", "part_of_speech"])
vocabulary_manager.merge_entries()
vocabulary_manager.create_tsv(file_path="./results.tsv")

print("--- %s seconds ---" % (time.time() - start_time))
