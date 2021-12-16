import csv
from functools import partial
import io

from click.testing import CliRunner
import pytest
from pytest_mock import MockerFixture

from .factories import KanjiFactory


@pytest.fixture
def cli():
    from wanikani_burnt_kanji_to_anki.__main__ import cli

    return partial(CliRunner(mix_stderr=False).invoke, cli, catch_exceptions=False)


def test_csv(cli, mocker: MockerFixture):
    expected_kanji = KanjiFactory.build_batch(5)

    mocker.patch("wanikani_burnt_kanji_to_anki.wanikani.WaniKaniAPIClient.load_kanji")
    mocker.patch(
        "wanikani_burnt_kanji_to_anki.wanikani.WaniKaniAPIClient.burnt_kanji",
        return_value=expected_kanji,
    )

    result = cli(["--wanikani-api-key=fake-key", "csv"])

    assert result.exit_code == 0

    reader = csv.reader(io.StringIO(result.stdout))
    assert list(reader) == [
        [kanji.characters, ", ".join(kanji.meanings), ", ".join(kanji.readings)]
        for kanji in expected_kanji
    ]
