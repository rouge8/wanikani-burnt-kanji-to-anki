from typing import ClassVar

import factory
import factory.fuzzy

from wanikani_burnt_kanji_to_anki.wanikani import _KANJI
from wanikani_burnt_kanji_to_anki.wanikani import Kanji


class KanjiFactory(factory.Factory):
    class Meta:
        model = Kanji

    id = factory.Sequence(lambda n: n)
    document_url = factory.Faker("url")
    characters = factory.fuzzy.FuzzyText(length=1)
    meanings: ClassVar[list[str]] = [
        "meaning1",
        "meaning2",
    ]
    readings: ClassVar[list[str]] = [
        "readings1",
        "readings2",
    ]

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = model_class(*args, **kwargs)

        _KANJI[instance.id] = instance

        return instance
