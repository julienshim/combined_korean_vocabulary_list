import csv
import os
import re

import utils.language_utils as language_utils


class DataManager:
    def __init__(self):
        self.entries = []

    def load_from_tsv_dir(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".tsv"):
                file_path = os.path.join(directory, filename)
                self.load_from_tsv_file(file_path)

    def load_from_tsv_file(self, file_path):
        with open(file_path, "r", newline="") as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter="\t")
            for row in reader:
                processed_res = self._process_entry(row)
                self.entries += processed_res

    def _process_entry(self, entry):
        results = []
        """
        NIKL
        '순위' means 'Rank'

        A. '등급' means 'Grade' or 'Level'
        B. '단어' means 'Word'
        C. '품사' means 'Part of Speech'
        D. '풀이' means 'Definition' or 'Explanation'
        
        TOPIK
        A. '수준' means 'Level'
        B. '어휘' means 'Vocabulary'
        C. '품사' means 'Part of Speech'
        D. '길잡이말' means 'Guide Phrase' or 'Example Usage'
        """

        pos_res = self._process_part_of_speech(entry.get("품사"))
        explanation_res = self._process_explanation(
            entry.get("풀이") or entry.get("길잡이말") or ""
        )
        for pos in pos_res:
            tmp = {}
            tmp["rank"] = entry.get("순위") or ""
            tmp["level"] = entry.get("등급") or entry.get("수준") or ""
            tmp["word"] = entry.get("단어") or entry.get("어휘") or ""
            tmp["part_of_speech"] = pos or ""
            tmp["explanation"] = explanation_res["explanation"]
            tmp["hanja"] = explanation_res["hanja"]
            results.append(tmp)

        return results

    def _process_part_of_speech(self, part_of_speech):
        """
        Investigate the following later:
        # - 의존명사 (Dependent Noun)
        # - 접사 (Affix)
        # - "줄어든 말" (Abbreviated Word)
        """

        part_of_speech_reference = {
            # go part of speech
            "감": "감탄사",
            "고": "고유 명사",
            "관": "관형사",
            "대": "대명사",
            "동": "동사",
            "명": "명사",
            "보": "보조 용언",
            "부": "부사",
            "불": "줄어든 말",  # corrected from '분석 불능'
            "수": "수사",
            "의": "의존명사",  # corrected from '의존 명사'
            "형": "형용사",
            # topik part of speech
            "감탄사": "감탄사",
            "관형사": "관형사",
            "관형사/수사": "관형사/수사",
            "관형사·명사": "관형사/명사",
            "관형사/대명사": "관형사/대명사",
            "대명사": "대명사",
            "대명사/부사": "대명사/부사",
            "대명사/관형사": "대명사/관형사",
            "대명사/명사": "대명사/명사",
            "대명사/감탄사": "대명사/감탄사",
            "동사": "동사",
            "동사/형용사": "동사/형용사",
            "명사": "명사",
            "명사/관형사": "명사/관형사",
            "명사/대명사": "명사/대명사",
            "명사/부사": "명사/부사",
            "명사/의존명사": "명사/의존명사",
            "명사/감탄사": "명사/감탄사",
            "부사": "부사",
            "부사/감탄사": "부사/감탄사",
            "부사/관형사·명사": "부사/관형사/명사",
            "부사/명사": "부사/명사",
            "수사": "수사",
            "수사/명사": "수사/명사",
            "수사·관형사": "수사/관형사",
            "수사/관형사": "수사/관형사",
            "수사·관형사/명사": "수사/관형사/명사",
            "수사·관형사/명사/부사": "수사/관형사/명사/부사",
            "의존명사": "의존명사",
            "의존명사/명사": "의존명사/명사",
            "접사": "접사",
            "줄어든 말": "줄어든 말",
            "형용사": "형용사",
            "형용사/동사": "형용사/동사",
            "조사": "조사",
        }

        return part_of_speech_reference[part_of_speech].split("/")

    def _process_explanation(self, explanation):

        result = {"explanation": explanation, "hanja": ""}

        if not explanation:
            return result

        error_reference = {
            "를 g다": "를 하다",
            "에서 연습핟": "에서 연습하다",
            "경찰 수가": "경찰 수사",
            "대적할 만함": "대적할 만한",
        }

        # Error Correction
        explanation = (
            error_reference[explanation]
            if explanation in error_reference
            else explanation
        )

        # Handle Hanja
        if language_utils.detect_languages(
            text=explanation, languages_to_detect=["hanja"]
        )["hanja"]:
            # Case 1 - Has Period
            if re.search(r"\.", explanation):
                h, e = explanation.split(".")
                result["hanja"] = h.strip()
                result["explanation"] = e.strip()
            else:
                # Case 2 - Has English
                if language_utils.detect_languages(
                    text=explanation, languages_to_detect=["english"]
                )["english"]:
                    split_result = language_utils.split_text(
                        text=explanation, split_types=["english", "hanja"]
                    )
                    result["hanja"] = split_result["hanja"].strip()
                    result["explanation"] = split_result["english"].strip()
                # Case 3 - Pure Hanja
                else:
                    result["hanja"] = explanation.strip()
                    result["explanation"] = ""

        return result

    def get_entries(self):
        return self.entries
