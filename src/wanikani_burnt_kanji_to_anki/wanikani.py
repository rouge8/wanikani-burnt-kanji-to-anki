from collections.abc import Iterable
import time
import typing

import attrs
import httpx
import structlog

log = structlog.get_logger()


@attrs.frozen
class Kanji:
    id: int
    document_url: str
    characters: str
    meanings: list[str]
    readings: list[str]


_KANJI: dict[int, Kanji] = {}


@attrs.frozen
class WaniKaniAPIClient:
    BASE_URL = "https://api.wanikani.com/v2"

    api_key: str = attrs.field(repr=False)
    client: httpx.Client = attrs.field(factory=httpx.Client)

    def __attrs_post_init__(self) -> None:
        self.client.headers.update({"Wanikani-Revision": "20170710"})

    def _request(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        log.info("requesting", path=path, params=params)
        start = time.time()
        resp = self.client.get(
            f"{self.BASE_URL}/{path}",
            params=params,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        end = time.time()
        log.info(
            "requested",
            path=path,
            params=params,
            status_code=resp.status_code,
            duration=end - start,
        )
        resp.raise_for_status()
        return resp

    def _paginated_request(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> Iterable[dict[str, typing.Any]]:
        next_url = path

        while next_url is not None:
            resp = self._request(next_url, params)
            resp = resp.json()

            next_url = resp["pages"]["next_url"]
            if next_url is not None:
                next_url = next_url.split(f"{self.BASE_URL}/", 1)[1]

            yield from resp["data"]

    def load_kanji(self) -> None:
        """Load all Kanji into memory."""
        for kanji in self._paginated_request(
            "subjects",
            {"types": "kanji", "hidden": "false"},
        ):
            _KANJI[kanji["id"]] = Kanji(
                id=kanji["id"],
                document_url=kanji["data"]["document_url"],
                characters=kanji["data"]["characters"],
                meanings=[
                    meaning["meaning"]
                    for meaning in kanji["data"]["meanings"]
                    if meaning["accepted_answer"]
                ],
                readings=[
                    reading["reading"]
                    for reading in kanji["data"]["readings"]
                    if reading["primary"] or reading["accepted_answer"]
                ],
            )

    def burnt_kanji(self) -> Iterable[Kanji]:
        """
        Get all burnt Kanji.

        Must be called after loading the Kanji data into memory with
        :meth:`~.load_kanji`.
        """
        for assignment in self._paginated_request(
            "assignments",
            {"subject_types": "kanji", "burned": "true", "hidden": "false"},
        ):
            yield _KANJI[assignment["data"]["subject_id"]]

    def get_kanji(self, kanji: str) -> Kanji:
        """
        Look up an individual Kanji.

        Must be called after loading the Kanji data into memory with
        :meth:`~.load_kanji`.
        """
        return next(  # pragma: no branch
            k for k in _KANJI.values() if k.characters == kanji
        )
