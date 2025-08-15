import csv
from functools import partial
import io
from pathlib import Path

from click.testing import CliRunner
from click.testing import Result
import pytest
from pytest_mock import MockerFixture

from .factories import KanjiFactory


@pytest.fixture
def cli() -> partial[Result]:
    from wanikani_burnt_kanji_to_anki.__main__ import cli

    return partial(CliRunner().invoke, cli, catch_exceptions=False)


@pytest.mark.parametrize("has_additional_kanji", [True, False])
def test_csv(
    has_additional_kanji: bool,
    cli: partial[Result],
    mocker: MockerFixture,
    tmp_path: Path,
) -> None:
    expected_kanji = KanjiFactory.build_batch(5)

    if has_additional_kanji:
        additional_kanji = KanjiFactory.create_batch(2)
        additional_kanji_file = tmp_path / "more-kanji.txt"
        with open(additional_kanji_file, "w") as f:
            for kanji in additional_kanji:
                print(kanji.characters, file=f)
    else:
        additional_kanji = []

    mocker.patch("wanikani_burnt_kanji_to_anki.wanikani.WaniKaniAPIClient.load_kanji")
    mocker.patch(
        "wanikani_burnt_kanji_to_anki.wanikani.WaniKaniAPIClient.burnt_kanji",
        return_value=expected_kanji,
    )

    args = ["--wanikani-api-key=fake-key", "csv"]
    if has_additional_kanji:
        args += ["--additional-kanji", str(additional_kanji_file)]

    result = cli(args)

    assert result.exit_code == 0

    reader = csv.reader(io.StringIO(result.stdout))
    assert list(reader) == [
        [kanji.characters, ", ".join(kanji.meanings), ", ".join(kanji.readings)]
        for kanji in expected_kanji + additional_kanji
    ]
