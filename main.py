import argparse
import time

import managers.data_manager as data_manager
import managers.merge_manager as merge_manager

start_time: float = time.time()


def main(results_tsv: str, nikl_tsv: str, topik_dir: str) -> None:
    # Date Managers
    nikl_data_manager = data_manager.DataManager()
    nikl_data_manager.load_from_tsv_file(file_path=nikl_tsv)
    nikl_data: list[dict[str, str]] = nikl_data_manager.get_entries()

    topik_data_manager = data_manager.DataManager()
    topik_data_manager.load_from_tsv_dir(directory=topik_dir)
    topik_data: list[dict[str, str]] = topik_data_manager.get_entries()

    # Merge Manager
    vocabulary_manager = merge_manager.MergeManager()
    vocabulary_manager.load_entries(entries=nikl_data)
    vocabulary_manager.load_entries(entries=topik_data)
    vocabulary_manager.sort_entries_by_keys(sorting_keys=["word", "part_of_speech"])
    vocabulary_manager.merge_entries()
    vocabulary_manager.create_tsv(file_path=results_tsv)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process vocabulary data.")
    parser.add_argument(
        "-r",
        "--results-tsv",
        type=str,
        default="./results.tsv",
        help="Specify the path for the results TSV file",
    )
    parser.add_argument(
        "-n", "--nikl-tsv", type=str, required=True, help="Path to the NIKL TSV file"
    )
    parser.add_argument(
        "-t",
        "--topik-dir",
        type=str,
        required=True,
        help="Path to directory containing TOPIK TSV files",
    )
    return parser


if __name__ == "__main__":
    parser: argparse.ArgumentParser = create_parser()
    args: argparse.Namespace = parser.parse_args()
    main(
        results_tsv=args.results_tsv,
        nikl_tsv=args.nikl_tsv,
        topik_dir=args.topik_dir,
    )

print("--- %s seconds ---" % (time.time() - start_time))
