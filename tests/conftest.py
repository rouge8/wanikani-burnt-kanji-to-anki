import pytest

from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient


@pytest.fixture
def api_client() -> WaniKaniAPIClient:
    """A WaniKaniAPIClient"""
    return WaniKaniAPIClient("fake-key")


@pytest.fixture(autouse=True)
def reset_kanji_cache() -> None:
    """Reset the Kanji cache between tests."""
    from wanikani_burnt_kanji_to_anki.wanikani import _KANJI

    _KANJI.clear()
