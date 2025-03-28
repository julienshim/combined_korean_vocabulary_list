import os
import shutil
from pathlib import Path

import pytest

from main import main


@pytest.fixture(scope="session")
def session_temp_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp(".tmp_test_dir")


def test_main_function_generates_target_tsv(session_temp_dir: Path) -> None:
    # Act
    tmp_results_tsv: str = os.path.join(session_temp_dir, "results.tsv")

    tmp_nikl_tsv: str = os.path.join(session_temp_dir, "nikl.tsv")
    shutil.copy2(
        "/path/to/nikl_tsv.tsv",
        tmp_nikl_tsv,
    )

    tmp_topik_dir: str = os.path.join(session_temp_dir, "topik")
    shutil.copytree(
        "/path/to/topik_dir",
        tmp_topik_dir,
    )

    main(results_tsv=tmp_results_tsv, nikl_tsv=tmp_nikl_tsv, topik_dir=tmp_topik_dir)

    # Assert
    assert os.path.exists(os.path.join(session_temp_dir, "results.tsv"))

    with open(tmp_results_tsv, "r", encoding="utf-8") as f:
        content: list[str] = f.read().splitlines()
        assert (
            content[0]
            == "rank\tword\tpart_of_speech\thanja\texplanation\tnikl_level\ttopik_level"
        )
        assert len(content) == 7498
