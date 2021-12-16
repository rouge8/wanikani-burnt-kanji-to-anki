import pytest


@pytest.fixture
def api_client():
    """A WaniKaniAPIClient"""
    from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient

    return WaniKaniAPIClient("fake-key")


@pytest.fixture(autouse=True)
def reset_kanji_cache():
    """Reset the Kanji cache between tests."""
    from wanikani_burnt_kanji_to_anki.wanikani import _KANJI

    _KANJI.clear()
