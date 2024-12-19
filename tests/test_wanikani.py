import faker
from httpx import URL
import pytest
from pytest_httpx import HTTPXMock

from wanikani_burnt_kanji_to_anki.wanikani import _KANJI
from wanikani_burnt_kanji_to_anki.wanikani import Kanji
from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient

from .factories import KanjiFactory


class TestWaniKaniAPIClient:
    @pytest.fixture
    def headers(self, api_client: WaniKaniAPIClient) -> dict[str, str]:
        return dict(api_client.client.headers) | {
            "Authorization": f"Bearer {api_client.api_key}",
        }

    def test_load_kanji(
        self,
        headers: dict[str, str],
        api_client: WaniKaniAPIClient,
        httpx_mock: HTTPXMock,
        faker: faker.proxy.Faker,
    ) -> None:
        assert not _KANJI, "Kanji cache has already been populated!"

        kanji = [
            {
                "id": faker.random_int(),
                "object": "kanji",
                "data": {
                    "document_url": faker.url(),
                    "characters": faker.pystr(),
                    "meanings": [
                        {
                            "meaning": faker.word(),
                            "primary": faker.pybool(),
                            "accepted_answer": faker.pybool(),
                        }
                        for _ in range(faker.random_int(min=1, max=3))
                    ],
                    "readings": [
                        {
                            "type": faker.word(),
                            "primary": faker.pybool(),
                            "reading": faker.pystr(),
                            "accepted_answer": faker.pybool(),
                        }
                        for _ in range(faker.random_int(min=1, max=5))
                    ],
                },
            }
            for _ in range(faker.random_int(min=3, max=10))
        ]
        expected_kanji = {
            k["id"]: Kanji(
                id=k["id"],
                document_url=k["data"]["document_url"],
                characters=k["data"]["characters"],
                meanings=[
                    meaning["meaning"]
                    for meaning in k["data"]["meanings"]
                    if meaning["accepted_answer"]
                ],
                readings=[
                    reading["reading"]
                    for reading in k["data"]["readings"]
                    if reading["primary"] or reading["accepted_answer"]
                ],
            )
            for k in kanji
        }

        httpx_mock.add_response(
            url=URL(
                f"{api_client.BASE_URL}/subjects",
                params={"types": "kanji", "hidden": "false"},
            ),
            headers=headers,
            json={
                "pages": {
                    "next_url": f"{api_client.BASE_URL}/subjects?types=kanji&hidden=false&page_after_id=12345",  # noqa: E501
                },
                "data": [kanji[0]],
            },
        )
        httpx_mock.add_response(
            url=URL(
                f"{api_client.BASE_URL}/subjects",
                params={"types": "kanji", "hidden": "false", "page_after_id": "12345"},
            ),
            headers=headers,
            json={
                "pages": {
                    "next_url": None,
                },
                "data": kanji[1:],
            },
        )

        api_client.load_kanji()
        assert _KANJI == expected_kanji

    def test_burnt_kanji(
        self,
        headers: dict[str, str],
        api_client: WaniKaniAPIClient,
        httpx_mock: HTTPXMock,
        faker: faker.proxy.Faker,
    ) -> None:
        expected_kanji = KanjiFactory.create_batch(faker.random_int(min=3, max=10))

        assignments = [
            {
                "id": faker.random_int(),
                "object": "assignment",
                "data": {"subject_id": kanji.id},
            }
            for kanji in expected_kanji
        ]

        httpx_mock.add_response(
            url=URL(
                f"{api_client.BASE_URL}/assignments",
                params={"subject_types": "kanji", "burned": "true", "hidden": "false"},
            ),
            headers=headers,
            json={
                "pages": {
                    "next_url": None,
                },
                "data": assignments,
            },
        )

        assert list(api_client.burnt_kanji()) == expected_kanji

    def test_get_kanji(self, api_client: WaniKaniAPIClient) -> None:
        random_kanji = KanjiFactory.create_batch(5)

        for kanji in random_kanji:
            assert api_client.get_kanji(kanji.characters) == kanji
