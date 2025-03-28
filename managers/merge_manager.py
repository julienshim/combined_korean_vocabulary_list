import csv
import re
from collections import defaultdict


class MergeManager:
    def __init__(self) -> None:
        self.entries: list[dict[str, str]] = []

    def load_entries(self, entries: list[dict[str, str]]) -> None:
        self.entries += entries

    def sort_entries_by_keys(self, sorting_keys: list[str], reverse: bool = False):
        result: list[dict[str, str]] = sorted(
            self.entries,
            key=lambda x: tuple(x.get(k, None) for k in sorting_keys),
            reverse=reverse,
        )
        self.entries = result

    def get_entries(self) -> list[dict[str, str]]:
        return self.entries

    def _compare_and_return_longest(self, entries: list[str]) -> list[str]:
        if not entries:
            return []

        longest = max(entries, key=len)

        for value in entries:
            if value != longest and value in longest:
                return [longest]

        return entries  # Return original list if no match found

    def _merge_entry_values(self, entries: list[dict[str, str]]) -> dict[str, str]:
        new_entry: dict[str, str] = {}

        nikl: dict[str, str] = entries[0]
        topik: dict[str, str] = entries[1]

        new_entry["rank"] = (  # only topik has a rank
            topik.get("rank") or nikl.get("rank") or ""
        )
        new_entry["level"] = nikl.get("level") or topik.get("level") or ""
        # Explanded levels
        new_entry["nikl_level"] = nikl.get("level") or ""
        new_entry["topik_level"] = topik.get("level") or ""
        new_entry["word"] = nikl.get("word") or topik.get("word") or ""
        new_entry["part_of_speech"] = (
            nikl.get("part_of_speech") or topik.get("part_of_speech") or ""
        )
        explanation_filtered = [
            explanation
            for explanation in [nikl.get("explanation"), topik.get("explanation")]
            if explanation is not None
        ]

        # Combine 1:1
        explanation_filtered: list[str] = list(set(explanation_filtered))

        # Return Long if Short in Longest
        explanation_filtered = self._compare_and_return_longest(explanation_filtered)
        explanation_filtered.sort()

        new_entry["explanation"] = (
            f'{"; " if len(explanation_filtered) > 1 else ""}'.join(
                explanation_filtered
            ).strip()
        )
        new_entry["hanja"] = (  # nikl should have it
            nikl.get("hanja") or topik.get("hanja") or ""
        )

        return new_entry

    def _expand_entries(self, entries: list[dict[str, str]]) -> list[dict[str, str]]:
        expanded_entries: list[dict[str, str]] = []
        for entry in entries:
            expanded_entry: dict[str, str] = entry.copy()
            is_topik = bool(re.search(r"[abcABC]", entry["level"]))
            expanded_entry["topik_level"] = entry["level"] if is_topik else ""
            expanded_entry["nikl_level"] = "" if is_topik else entry["level"]
            expanded_entries.append(expanded_entry)
        return expanded_entries

    def merge_entries(self) -> None:
        results: list[dict[str, str]] = []
        # Merge - Step 1: Map Vocabulary Data by Word (Numberless)
        data_map: defaultdict[str, defaultdict[str, list[dict[str, str]]]] = (
            defaultdict(lambda: defaultdict(list))
        )
        for entry in self.entries:
            """
            I found that there is not reason to remove the number of word entries
            because when we merge and count for alpha level count,
            it always ends in a 0 (all nikl) or 2 (all TOPIK).
            See alpha_level_count below.
            """
            # word_numberless = re.sub(r"[0-9]+", "", entry["word"])
            data_map[entry["word"]][entry["part_of_speech"]].append(entry)

        for _, word_dict in data_map.items():
            for _, entries in word_dict.items():
                # Merge - Step 2: Handle lists of 2
                if len(entries) == 2:
                    """
                    Test to see if we have 1 nikl entry and 1 TOPIK entry in each entries list
                    YES - If we keep the number in word entries.
                    No need to remove number per anote above.

                    """
                    # alpha_level_count = len(
                    #     list(filter(lambda x: re.search(r"[a-z]", x["level"].lower()), entries))
                    # )
                    # if alpha_level_count != 1:
                    #     print(alpha_level_count, entries)
                    """Skip to sorting"""
                    entries: list[dict[str, str]] = sorted(
                        entries, key=lambda x: x["level"], reverse=True
                    )
                    merged_entry: dict[str, str] = self._merge_entry_values(entries)
                    results += [merged_entry]
                else:
                    expanded_entries = self._expand_entries(entries)
                    results += expanded_entries
        self.entries = results

    def create_tsv(self, file_path: str):
        data: list[dict[str, str]] = sorted(
            self.entries,
            key=lambda x: re.sub(
                r"[^\uAC00-\uD7A3\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]",
                "",
                x["word"],
            ),
        )
        with open(file_path, "w") as f:
            headers = [
                "rank",
                "word",
                "part_of_speech",
                "hanja",
                "explanation",
                "nikl_level",
                "topik_level",
            ]
            tsv_writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t")
            tsv_writer.writeheader()

            for entry in data:
                del entry["level"]
                tsv_writer.writerow(entry)

        print(f"Results written to {file_path}...")
